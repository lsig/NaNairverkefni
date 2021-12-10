from storage_layer.DLAPI import DlAPI
from models.report import Report
from datetime import datetime
from logic_layer.jobLL import JobLL

# NOTETOSELF - sum verk krefjast verktaka, en ekki öll. Td gluggaþvottur krefst ekki en að laga pípulagnir krefst þess. 
# Ef verktaki er nauðsynlegur, þarf að taka fram þóknun verktaka, en ekki þarf að gera það ef enginn verktaki er ráðinn.

class ReportsLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.jobll = JobLL()
    #Adds report to the report.csv file. Validates if everything is correct first
    def add_report(self, rep_dic, job_dic): 
        cont_dic = self.dlapi.get_all_cont()
        rep_dic['Contractor-rating'] = ''#reports starts with no rating
        rep_dic["Feedback"] = 'None' #report starts with no Feedback 
        valid, key = self.report_validation(rep_dic,job_dic)
        if valid:
            current_date = datetime.date(datetime.now())
            rep = Report(self.generate_id(), job_dic["id"],job_dic["Employee"],job_dic["Employee-id"],job_dic["Title"],rep_dic["Description"],job_dic["Location"], job_dic["Property"], job_dic["Property-number"], job_dic["Property-id"], self.get_cont_name(rep_dic["Contractor-id"]), rep_dic["Contractor-id"], rep_dic["Contractor-rating"], current_date, rep_dic["Commission"],rep_dic["Total-cost"], "0",rep_dic["Feedback"])
            #Generated info and info from user added to the model
            self.dlapi.add_report(rep)#report created in csv
            return True, key
        return False, key #bounces back if user input is wrong

    def generate_id(self): #Auto incremented id for new report
        all_rep_lis = self.dlapi.get_all_report()
        if all_rep_lis == []:
            new_id = 1
        else:
            new_id = int(all_rep_lis[len(all_rep_lis)-1]["Report-id"])+1
        return str(new_id)#returns generated id

    # def list_all_reports(self): #klárt Líklegast useless þar sem get_all_rep gerir það sama núna
    #     all_rep = self.dlapi.get_all_report()
    #     return all_rep


    def edit_report_info(self, edit_rep_dic): # klárt useless!
        # NOTETOSELF:yfirmaður þarf að geta samþykkt viðhaldsskýrslur, og starfsmenn þurfa að geta séð hvaða skýrslur, sem þeir eiga, eru samþykktar og hverjar ekki.
        # Ef skýrsla er ekki samþykkt, þarf starfsmaður að geta breytt upplýsingum í skýrslunni.
        if self.report_validation(edit_rep_dic):
            #rep_dic = rep_dic["Status"] = "1"
            all_rep_lis = self.dlapi.get_all_report()
            dic = self.find_rep_id(edit_rep_dic["Report-id"], all_rep_lis)
            rep_loc_in_list = self.find_id_location_rep(dic, all_rep_lis)
            all_rep_lis[rep_loc_in_list] = edit_rep_dic
            self.dlapi.change_report(all_rep_lis)
            return True
        return None

        # NOTETOSELF: Skýrslur merktar "pending", "accepted", eða "rejected"
        # yfirmaður getur merkt skýrslu accepted eða rejected, en starfsmaður getur merkt skýrslu pending.
        # # # 

    def get_all_rep(self): #Gets all reports from csv file
        all_reports = self.dlapi.get_all_report()
        return all_reports
    

    def sort_all_reports(self):#gets all reports from csv and sorts them by status
        all_reports = self.get_all_rep()
        finished_reports = []
        pending_reports = []
        other_reports = []
        for report in all_reports:
            if report['Status'] == '2':
                finished_reports.append(report)

            elif report['Status'] == '1':
                pending_reports.append(report)
            
            else:
                other_reports.append(report)
        
        return [pending_reports, finished_reports, other_reports]
    
    def get_property_reports(self, propertyid):#reports by property id
        propertyreports = []
        all_reports = self.get_all_rep()
        for report in all_reports:
            if report['Property-id'] == propertyid:
                propertyreports.append(report)
        return propertyreports
    
    def get_emp_reports(self, empid):#reports by employee-id
        empreports = []
        all_reports = self.get_all_rep()
        for report in all_reports:
            if report['Employee-id'] == empid:
                empreports.append(report)
        return empreports
    
    def get_contractor_reports(self, contractorid):#reports by contractor id
        contractorreports = []
        all_reports = self.get_all_rep()
        for report in all_reports:
            if report['Contractor-id'] == contractorid:
                contractorreports.append(report)
        return contractorreports
            




    def get_report_name_and_location(self,id): #klárt líklegast useless nýtist ekki
        rep_lis = self.dlapi.get_all_report()
        for dic in rep_lis:
            if int(id) == int(dic["Report-id"]):
                rep_info = {"Name":dic["Name"],"Location":dic["Location"]}
                return rep_info        
        rep_info = {"Name":"null","Location":"null"}
        return rep_info 

#finds correct list index. For changing specific line in the the csv file, used for changing information the the csv file
    def find_id_location_rep(self, dic, all_rep_lis):
        for i in range(len(all_rep_lis)):
            if dic == all_rep_lis[i]:
                return i
            
    #searches after correct dictionary in the list of dictionaries is used for changing csv file
    def find_rep_id(self, id, all_rep_lis, key):
        if id.isdigit():
            for dic in all_rep_lis:
                if int(dic[key]) == int(id):
                    dic = dic
                    return dic
            return None
        return False



#This function takes in report_dictionary from the ui layer and changes status of the report and the job according to the action performed by the user
    def confirm_and_ready_report_and_grade_contractor(self, rep_dic): # klárað #.replace(' ','')
        all_rep_lis = self.dlapi.get_all_report()
        dic = self.find_rep_id(rep_dic["Report-id"], all_rep_lis, "Report-id")
        if dic["Status"] == "0" and rep_dic["Status"] == "0": #Used to change report without making it ready. Possible feature
            rep_loc_in_list = self.find_id_location_rep(dic, all_rep_lis)
            dic = rep_dic
            all_rep_lis[rep_loc_in_list] = dic
            self.dlapi.change_report(all_rep_lis)
        if dic["Status"] == "0" and rep_dic["Status"] == "1": #if staus was (0=not ready) and now (1=ready) markes job as ready for confirmation by the boss 
            rep_loc_in_list = self.find_id_location_rep(dic, all_rep_lis)
            dic = rep_dic
            dic["Status"] = "1"
            dic["Feedback"] = ""
            all_rep_lis[rep_loc_in_list] = dic
            self.dlapi.change_report(all_rep_lis)
            all_job_lis = self.jobll.get_all_jobs()
            job = self.find_rep_id(rep_dic["Request-id"], all_job_lis,"id")
            job["Status"] = "1"
            self.jobll.edit_info(job,rep_dic["Request-id"])           


        if dic["Status"] == "1" and rep_dic["Status"] == "2": #Markes report and job as completed, with feedback
            rep_loc_in_list = self.find_id_location_rep(dic, all_rep_lis)
            dic = rep_dic
            dic["Status"] = "2"
            all_rep_lis[rep_loc_in_list] = dic
            self.dlapi.change_report(all_rep_lis)
            all_job_lis = self.jobll.get_all_jobs()
            job = self.find_rep_id(rep_dic["Request-id"], all_job_lis,"id")
            job["Status"] = "2"
            self.jobll.edit_info(job,rep_dic["Request-id"])          
#Reopems job and report, if boss wants to reopen the job. Declines report, with Feedback
        if dic["Status"] == "2" and rep_dic["Status"] == "0" or dic["Status"] =="1" and rep_dic["Status"] == "0":
            # Reopen job and change status, request-id
            rep_loc_in_list = self.find_id_location_rep(dic, all_rep_lis)
            dic = rep_dic
            dic["Status"] = "0"
            all_rep_lis[rep_loc_in_list] = dic
            self.dlapi.change_report(all_rep_lis)
            all_job_lis = self.jobll.get_all_jobs()
            job = self.find_rep_id(rep_dic["Request-id"], all_job_lis,"id")
            job["Status"] = "0"
            self.jobll.edit_info(job,rep_dic["Request-id"])  
     
    

#Validates that everything is correct. Description not empty, checks if contractor is located in the same location as the property.
#check is commission is lower than Total-cost
    def report_validation(self, rep_dic,job_dic): # 
        cont_dic = self.dlapi.get_all_cont()
        get_validation = True
        # a dictionairy for title, description, contractor-name and contractor-id.
        dic = {"Description":"both", "Contractor-id":int, "Commission": int,"Total-cost":int}
        counter = 0
        prev = 0
        for key in dic.keys():
            if key == "Commission":
                if prev != "" and rep_dic[key] == "" or prev == "" and rep_dic[key] != "":
                    return False, key                
            # checking if the dictionairy key is a string and not both string and integer, and if so, remove spaces.
            if dic[key] == str and dic[key] != "both":
                get_validation = rep_dic[key].replace(" ", "").isalpha()
            # checking if the dictionairy key is an integer and not both string and integer, and if so, check if integer is in fact a number/digit.
            elif dic[key] == int and dic[key] != "both" and rep_dic[key] != "":
                get_validation = rep_dic[key].isdigit()
            # checking if the dictionairy key is both a string and integer, and if so, check if the key is empty. If so, the program will return False.
            if key == "Total-cost":
                if rep_dic["Commission"] != '' and rep_dic[key] <= rep_dic["Commission"]:
                    return False, key
            if dic[key] == "both":
                if rep_dic[key] == "":
                    return False, key

            if key == "Contractor-id" and get_validation:
                if rep_dic["Contractor-id"] != '':
                    con_id_bool,dic_con = self.check_cont_dic(rep_dic["Contractor-id"],cont_dic)
                    if con_id_bool == False:
                        return False,key
                    else:
                        if dic_con["Location"] != job_dic["Location"]:
                            return False,key
            if get_validation == False:
                    return False, key
            prev = rep_dic[key]
        return True, None

    def check_cont_dic(self,cont_id,cont_dic):#checks if contractor is in database and returns his dic
        for dic in cont_dic:
            if dic["id"] == cont_id:
                return True,dic     
        return False

    def find_rep_by_str(self,user_string,rep_lis,key):#search engine which searches by dic key
        ret_lis=[]
        for dic in rep_lis:
            if user_string.lower() in dic[key].lower():
                ret_lis.append(dic)
        if ret_lis == []:
            return False #skoða þetta svo filter drepur ekki forritið
        return ret_lis

    def find_rep_id(self,id,all_rep_lis,key):#Find one report with exact id
        if id.isdigit():
            for dic in all_rep_lis:
                if int(dic[key]) == int(id):
                    dic = dic
                    return dic 
            return None #[{"Text":"No employee with this id"}]
        return False
    
    def find_rep_id_2(self,id):#used for confimation and declining of reports
        all_rep = self.get_all_rep()
        for dic in all_rep:
            if dic['Request-id'] == id:
                return dic

    def get_cont_name(self,cont_id):#gets contractor name from id
        all_cont_lis = self.dlapi.get_all_cont()
        for cont_dic in all_cont_lis:
            if cont_dic["id"] == cont_id:
                return cont_dic["Name"]
        return ""



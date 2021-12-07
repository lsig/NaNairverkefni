from storage_layer.DLAPI import DlAPI
from models.report import Report
from datetime import datetime

# NOTETOSELF - sum verk krefjast verktaka, en ekki öll. Td gluggaþvottur krefst ekki en að laga pípulagnir krefst þess. 
# Ef verktaki er nauðsynlegur, þarf að taka fram þóknun verktaka, en ekki þarf að gera það ef enginn verktaki er ráðinn.

class ReportsLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_report(self, rep_dic, job_dic):
        cont_dic = self.dlapi.get_all_cont()
        if self.report_validation(rep_dic, cont_dic):
            current_date = datetime.date(datetime.now())
            #rep_dic = self.replace_loc_num_with_name(rep_dic)
            rep = Report(self.generate_id(), job_dic["id"],job_dic["Employee"],job_dic["Employee-id"],rep_dic["Title"],rep_dic["Description"],job_dic["Location"], job_dic["Property"], job_dic["Property-number"], job_dic["Property-id"], rep_dic["Contractor-name"], rep_dic["Contractor-id"], rep_dic["Contractor-rating"], current_date, rep_dic["Commission"], "0")
            # Status, Property, Property-number, Property-id, Contractor-Rating, Location
            self.dlapi.add_report(rep)
            return True
        return False

    def generate_id(self):
        all_rep_lis = self.dlapi.get_all_report()
        if all_rep_lis == []:
            new_id = 1
        else:
            new_id = int(all_rep_lis[len(all_rep_lis)-1]["id"])+1
        return str(new_id)

    def list_all_reports(self):
        all_rep = self.dlapi.get_all_report()
        return all_rep

    def edit_report_info(self, edit_rep_dic):
        # NOTETOSELF:yfirmaður þarf að geta samþykkt viðhaldsskýrslur, og starfsmenn þurfa að geta séð hvaða skýrslur, sem þeir eiga, eru samþykktar og hverjar ekki.
        # Ef skýrsla er ekki samþykkt, þarf starfsmaður að geta breytt upplýsingum í skýrslunni.
        if self.report_validation(edit_rep_dic):
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

    def get_all_rep(self):
        all_reports = self.dlapi.get_all_report()
        counter = 0
        for i in all_reports:
            all_reports[counter]["Suggested-contractor"] = self.get_report_name_and_location(i["Suggested-contractor"])["Name"]
            counter += 1
        return all_reports

    def get_report_name_and_location(self,id):
        rep_lis = self.dlapi.get_all_report()
        for dic in rep_lis:
            if int(id) == int(dic["Report-id"]):
                rep_info = {"Name":dic["Name"],"Location":dic["Location"]}
                return rep_info        
        rep_info = {"Name":"null","Location":"null"}
        return rep_info 

    def find_id_location_rep(self, dic, all_rep_lis):
        for i in range(len(all_rep_lis)):
            if dic == all_rep_lis[i]:
                return i
            
    def find_rep_id(self, all_rep_lis):
        if id.isdigit():
            for dic in all_rep_lis:
                if int(dic["Report-id"]) == int(id):
                    return dic
            return None
        return False

<<<<<<< HEAD
    def find_id_location_con(self, dic, all_con_lis):
        for i in range(len(all_con_lis)):
            if dic == all_con_lis[i]:
                return i


    def confirm_report(self, id):
        all_con_lis = self.dlapi.get_all_cont()
        for dic in all_con_lis:
            if dic["Report-id"] == id:
                dic = dic["Status"] = "2"
            
            con_loc_in_list = self.find_id_location_con(dic, all_con_lis)
            all_con_lis[con_loc_in_list] = dic
            self.dlapi.change_report(all_con_lis)
            


    def ready_report(self):
        pass

        # for dic in all_con_lis:
        #     if dic["id"] == id:
        #         rep_from_con = self.list_all_rep_from_con(id)
        #         avr_con_grade = self.calculate_average_con_grade(rep_from_con, all_con_lis)





    def calculate_average_con_grade(self):
        list_of_ratings = self.list_all_rep_from_con()
        if list_of_ratings is not None:
            average = sum(list_of_ratings)/len(list_of_ratings)
            return average        
    

    def list_all_rep_from_con(self, id):
        all_con_lis = self.dlapi.get_all_cont()
        ret_lis = []    
        if id.isdigit():
            for dic in all_con_lis:
                if int(dic["id"]) == int(id):
                    ret_lis.append(dic["Contractor-rating"])
        if len(ret_lis) != 0:
            return ret_lis
        else:
            return None


=======
>>>>>>> c649217a30c6327a41fd34d9dfa5a4c78de526d4
    def report_validation(self, rep_dic, cont_dic):
        # a dictionairy for title, description, contractor-name and contractor-id.
        dic = {"Title":str, "Description":"both", "Contractor-id":int, "Commission": int}
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
            if dic[key] == "both":
                if rep_dic[key] == "":
                    return False, key
            if get_validation == False:
                    return False, key
            prev = rep_dic[key]
            return True

if __name__ == "__main__":
    r = ReportsLL()
    print("maxim er king")
    r.add_report({"Title":"Maxim", "Description":"something", "Priority":"ASAP", "Suggested-contractor":"1", "Contractor-name": "kris", "Contractor-id": "1", "Contractor-rating":"3", "Status":"0", "Commission":"5000"}, {"id":"1", "Date-created":"2021-12-06", "Employee":"Jacob Yxa", "Employee-id":"2", "Location":"Longyearbyen", "Property":"Vei 217", "Property-number":"F959594", "Property-id":"1"})
## id = 1
# Date-created = 2021-12-06
# Employee = Jacob Yxa
# Employee-id = 2
# Title = Maxim
# Description = something
# Location = Longyearbyen  
# Property = Vei 217
# Property-number = F959594
# Property-id = 1
# Priority = ASAP
# Suggested-contractor = 1
# Status = 0
#Report-id,Request-id,Employee,Employee-id,Title,Description,Location,Property,Property-number,Property-id,Contractor-name,Contractor-id,Contractor-Rating,Date,Commission,"Status

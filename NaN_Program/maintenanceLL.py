

from models.maintenance import Maintenance
from storage_layer.DLAPI import DlAPI
from EmployeeLL import EmployeeLL
from propertyLL import PropertyLL
from jobLL import JobLL
from datetime import date, datetime,timedelta


class MaintenanceLL:

    def __init__(self):
        self.dlapi = DlAPI()
        self.empLL = EmployeeLL()
        self.propLL = PropertyLL()
        self.jobLL = JobLL()
        self.boss_id = ""
        self.boss_loc = ""
        


    def add_maintenance(self,main_dic,boss_id):
        # id,Date-from,Date-to,Frequency,Employee,Employee-id,Title,Description,
        # Location,Property,Property-number,Property-id,Priority,Suggested-contractor,Status
        
        # dic_fromat = {"Date-to(dd-mm-yyyy)"":int,"Frequency":int,"Employee-id":int,"Title":str,"Description":"both","Property-id":int,"Priority":int,"Suggested-contractor":str}
        self.boss_loc = self.empLL.get_emp_location(boss_id)
        self.boss_id = boss_id
        curr_date = datetime.date(datetime.now())
        valid_bool,key = self.is_valid(curr_date,main_dic)
        if valid_bool:
            
            emp_name =self.empLL.find_employee_name(main_dic["Employee-id"])
            prop_addr,prop_nr = self.get_property_info(main_dic["Property-id"])
            cont_names = self.get_cont_names(main_dic["Suggested-contractor(id)"]) # þarf að bæta við þessu í dl
            # bæta við nöfnunum9
            main_job = Maintenance(self.assign_id(),curr_date,main_dic["Date-to(dd-mm-yyyy)"],main_dic["Frequency(Week: 1, or Month: 2)"],emp_name,main_dic["Employee-id"],main_dic["Title"],
            main_dic["Description"],self.boss_loc,prop_addr,prop_nr,main_dic["Property-id"],main_dic["Priority(ASAP; Now; Emergency)"],cont_names,main_dic["Suggested-contractor(id)"].replace(" ",""),"0")
            self.dlapi.add_maintenance_job(main_job)
            return True,key
        return False,key


    def assign_id(self):
        all_main_job = self.dlapi.get_maintenance_jobs()
        if all_main_job != []:
            new_id = int(all_main_job[len(all_main_job)-1]["id"])+1
            return str(new_id)
        return str(1)

    def is_valid(self,today,main_dic):
        dic = {"Date-to(dd-mm-yyyy)":int,"Frequency(Week: 1, or Month: 2)":int,"Employee-id":int,"Title":str,"Description":"both","Property-id":int,"Priority(ASAP; Now; Emergency)":str,"Suggested-contractor(id)":int}
        for key in dic.keys():
            if dic[key] == str:
                get_validation = main_dic[key].replace(" ", "").isalpha()
            elif dic[key] == int and key != "Suggested-contractor(id)":
                get_validation = main_dic[key].replace("-","").isdigit()  
            elif dic[key] == "both" and main_dic[key] == "":
                return False,key
            else:
                get_validation = True

            if key == "Date-to(dd-mm-yyyy)" and main_dic[key] != "":
                if len(main_dic[key]) != 10 and main_dic.split("-") != 3:
                    return False, key

                date_time = self.check_date(main_dic[key].split("-"))
                if date_time == False:
                    return False,key
            elif key == "Date-to(dd-mm-yyyy)" and main_dic[key] == "":
                date_time = 0
                get_validation = True

            if key == "Frequency(Week: 1, or Month: 2)":
                if int(main_dic[key]) == 1 or int(main_dic[key]) == 2:
                    pass
                else:
                    return False,key
            if key == "Employee-id" and get_validation :
                if str(self.boss_id) == main_dic["Employee-id"]:
                    return False,key
                emp_dic = self.find_emp(main_dic[key])
                if emp_dic == {} or emp_dic["Destination"] != self.boss_loc :
                    return False,key

            if key == "Property-id" and get_validation:
                prop_dic = self.get_property(main_dic[key])
                if prop_dic == {} or prop_dic["Destination"] != self.boss_loc:
                    return False,key
            if key == "Suggested-contractor(id)"  and main_dic[key] != "":
                get_validation = main_dic[key].replace(",","").replace(" ","").isdigit()
                if get_validation == False:
                    return False,key
                cont_booL = self.check_cont_dic(main_dic[key].replace(" ", "").split(","))
                if cont_booL == False:
                    return False,key
                    
            elif  key == "Suggested-contractor(id)" and main_dic[key] != "":
                get_validation = True

            
            if key == "Priority(ASAP,Now,Emergency)" and get_validation:
                if main_dic[key].lower() != "asap" and main_dic[key].lower() != "now" and main_dic[key].lower() != "emergency":
                    return False,key
                    
            if get_validation == False:
                    return False, key
        if main_dic["Frequency(Week: 1, or Month: 2)"] == "1":
            freq = 7
        else:
            freq = 30
        if   date_time != 0  and today >= date_time:
            if (date_time-today).days() <= freq:
                return False,"Date-to(dd-mm-yyyy)"
        return True,"" 


    def check_date(self,date):
        if len(date[0]) == 2 and len(date[1]) == 2 and len(date[2]) == 4:
            if int(date[0]) > 0 and int(date[0]) < 32 and int(date[1]) > 0 and int(date[1]) < 13:
                date_time=datetime(int(date[2]),int(date[1]),int(date[0])).date()
                if date_time > datetime.date(datetime.now()):
                    return date_time
        return False


    def find_emp(self,id):
        return self.empLL.find_emp_id(id,self.dlapi.get_all_emp())

    def get_property(self,id):
        return self.propLL.find_prop_id(id,self.dlapi.get_property_info())

    def check_cont_dic(self,id_lis):
        all_cont = self.dlapi.get_all_cont()
        counter = 0
        for dic in all_cont:
            for id in id_lis:
                if dic["id"] == id:
                    if dic["Location"] != self.boss_loc:
                        return False
                    else:
                        counter += 1
        if counter != len(id_lis):
            return False             
        return True
        


    def get_cont_names(self,conts_str):
        ret_str = ""
        if conts_str != "":
            all_conts_lis = self.dlapi.get_all_cont()
            conts_lis = "".join(conts_str.strip().split()).split(",")
            for dic in all_conts_lis:
                for id in conts_lis:
                    if dic["id"] == id:
                        ret_str += ","+str(dic["Name"])
        return ret_str.strip(",")


    def get_property_info(self,prop_id):
        prop_dic = self.get_property(prop_id)
        if prop_id != {}:
            return prop_dic["Address"],prop_dic["Property-number"]
        return " "," "

    def get_all_main_jobs(self):
        return self.dlapi.get_maintenance_jobs()

    def add_to_job(self):
        all_main_job_lis = self.get_all_main_jobs()
        self.update_status(all_main_job_lis)
        counter = 0
        for main_dic in all_main_job_lis:
            if main_dic["Status"] == "0":
                if main_dic["Frequency:Week(1) or Month(2)"] == "1":
                    freq = 7
                else:
                    freq= 30
                date_lis = main_dic["Date-from"].split("-")
                # print(date_lis)
                ref_date=(datetime(int(date_lis[0]),int(date_lis[1]),int(date_lis[2]))+ timedelta(days=freq)).date()
                today = datetime.date(datetime.now())
                if (ref_date-today).days <= 2:
                    add_to_job_dic = main_dic
                    main_dic["Date-from"] = ref_date
                    all_main_job_lis[counter] = main_dic
                    add_to_job_dic["Date-created"] = ref_date
                    self.jobLL.add_job(add_to_job_dic,None,True)
            counter += 1
        self.update_main_job(all_main_job_lis)

                    
            
        

    def update_status(self,all_main_jobs):
        counter = 0
        for main_dic in all_main_jobs:
            if main_dic["Date-to"] != "":
                date_lis = main_dic["Date-to"].split("-")
                date=datetime(int(date_lis[2]),int(date_lis[1]),int(date_lis[0])).date()
                today = datetime.date(datetime.now())
                if (date-today).days <= 0:
                    main_dic["Status"] = "1"
                    all_main_jobs[counter] = main_dic
            counter += 1
        self.update_main_job(all_main_jobs)
        
        
    def update_main_job(self,all_main_jobs):
        self.dlapi.change_maintenance_job(all_main_jobs)
        
    # þarf að bæta við search by sting 
if __name__ == "__main__":
    x1 = datetime.date(datetime.now())
    # print(x1)
    # date = "20-12-2000".split("-")
    # print(len(date))
    # # print(date)
    # x=datetime(int(date[2]),int(date[1]),int(date[0])).date()
    # print(x1>x)
    # # print(x)
    # print((x1- x).days)
    # print(x.strftime("%B"))

    dic_fromat = {"Date-to(dd-mm-yyyy)":"","Frequency(Week: 1, or Month: 2)":"1","Employee-id":"5","Title":"hani","Description":"hehe","Property-id":"2","Priority(ASAP,Now,Emergency)":"Asap","Suggested-contractor(id)":""}
    g = MaintenanceLL()
    # # print(dic_fromat[])
    print(g.add_maintenance(dic_fromat,4))
    # t =",S, i,                                        i"
    # a = " ".join(t.strip(",").split()).split(",")
    # print(a)
    # p = "".strip()
    # print(p,"yeahh")
    # lis = g.get_all_main_jobs()
    # print(lis[len(lis)-1])
    # if x:
    #     print("yeah")
    g.add_to_job()
    
    # print(g.get_all_main_jobs())
    # g.update_main_job(DlAPI.get_maintenance_jobs())
    # x1 = datetime.date(datetime.now())
    # x2 = x1+ timedelta(days=10)
    # print(x1,x2)
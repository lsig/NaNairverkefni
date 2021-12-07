from models.maintenance import Maintenance
from storage_layer.DLAPI import DlAPI
from EmployeeLL import EmployeeLL
from propertyLL import PropertyLL
from datetime import date, datetime


class MaintenanceLL:

    def __init__(self):
        self.dlapi = DlAPI()
        self.empLL = EmployeeLL()
        self.propLL = PropertyLL()
        


    def add_maintenance(self,main_dic,boss_id):
        # id,Date-from,Date-to,Frequency,Employee,Employee-id,Title,Description,
        # Location,Property,Property-number,Property-id,Priority,Suggested-contractor,Status
        
        # dic_fromat = {"Date-to(dd-mm-yyyy)"":int,"Frequency":int,"Employee-id":int,"Title":str,"Description":"both","Property-id":int,"Priority":int,"Suggested-contractor":str}
        boss_loc = 
        curr_date = datetime.date(datetime.now())
        valid_bool,key = self.is_valid(curr_date,main_dic)
        if valid_bool:
            
            emp_name =None
            boss_loc = None
            prop,prop_nr = None,None
            priority = None
            main_job = Maintenance(self.assign_id(),curr_date,main_dic["Date-to(dd-mm-yyyy)"],main_dic["Frequency:Week(1) or Month(2)"],emp_name,main_dic["Employee-id"],main_dic["Title"],
            main_dic["Description"],boss_loc,prop,prop_nr,main_dic["Property-id"],priority,main_dic["Suggested-contractor"],0)
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
        dic = {"Date-to(dd-mm-yyyy)":int,"Frequency:Week(1) or Month(2)":int,"Employee-id":int,"Title":str,"Description":"both","Property-id":int,"Priority":int,"Suggested-contractor":str}
        for key in dic.keys():
            if dic[key] == str:
                get_validation = main_dic[key].replace(" ", "").isalpha()
            elif dic[key] == int:
                print(main_dic[key])
                get_validation = main_dic[key].replace("-","").isdigit()  
            elif dic[key] == "both" and main_dic[key] == "":
                return False,key
            else:
                get_validation = True

            if key == "Date-to(dd-mm-yyyy)" and get_validation and main_dic[key] != "":
                if len(main_dic[key]) != 10:
                    return False, key

                date_time = self.check_date(main_dic[key].split("-"))
                if date_time:
                    pass
                else:
                    return False,key
            elif key == "Date-to(dd-mm-yyyy)" and main_dic[key] != "":
                get_validation = True

            if key == "Frequency:Week(1) or Month(2)":
                if int(main_dic[key]) == 1 or int(main_dic[key]) == 2:
                    pass
                else:
                    return False,key
            if key == "Employee-id" and get_validation:
                if self.find_emp(main_dic[key]) == {}:
                    return False,key

            if key == "Property-id" and get_validation:
                if self.get_property(main_dic[key]) == {}:
                    return False,key
            if key == "Suggested-contractor" and main_dic[key] == "":
                get_validation = True
                
            if get_validation == False:
                    return False, key
        if main_dic["Frequency:Week(1) or Month(2)"] == "1":
            freq = 7
        else:
            freq = 30
        if today >= date_time:
            if (date_time-today).days() <= freq:
                return False,"Date-to(dd-mm-yyyy)","Frequency"
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

    


if __name__ == "__main__":
    x1 = datetime.date(datetime.now())
    date = "20-12-2000".split("-")
    print(len(date))
    # print(date)
    x=datetime(int(date[2]),int(date[1]),int(date[0])).date()
    print(x1>x)
    # print(x)
    print((x1- x).days)
    # print(x.strftime("%B"))

    dic_fromat = {"Date-to(dd-mm-yyyy)":"20-12-2022","Frequency:Week(1) or Month(2)":"1","Employee-id":"2","Title":"hani","Description":"hehe","Property-id":"3","Priority":"1","Suggested-contractor":""}
    g = MaintenanceLL()
    # print(dic_fromat[])
    print(g.add_maintenance(dic_fromat,1))

    if x:
        print("yeah")
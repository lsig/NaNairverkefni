from models.maintenance import Maintenance
from storage_layer.DLAPI import DlAPI
from datetime import date, datetime


class MaintenanceLL:

    def __init__(self):
        self.dlapi = DlAPI()
        


    def add_maintenance(self,main_dic,boss_id):
        # id,Date-from,Date-to,Frequency,Employee,Employee-id,Title,Description,
        # Location,Property,Property-number,Property-id,Priority,Suggested-contractor,Status
        # dic_fromat = {"Date-to(dd-mm-yyyy)"":int,"Frequency":int,"Employee-id":int,"Title":str,"Description":"both","Property-id":int,"Priority":int,"Suggested-contractor":str}
        curr_date = datetime.date(datetime.now())
        emp_name =None
        boss_loc = None
        prop,prop_nr = None,None
        priority = None
        main_job = Maintenance(self.assign_id(),curr_date,main_dic["Date-to(dd-mm-yyyy)"],main_dic["Frequency:Week(1) or Month(2)"],emp_name,main_dic["Employee-id"],main_dic["Title"],
        main_dic["Description"],boss_loc,prop,prop_nr,main_dic["Property-id"],priority,main_dic["Suggested-contractor"],0)
        self.dlapi.add_maintenance_job(main_job)


    def assign_id(self):
        all_main_job = self.dlapi.get_maintenance_jobs()
        if all_main_job != []:
            new_id = int(all_main_job[len(all_main_job)-1]["id"])+1
            return str(new_id)
        return str(1)

    def is_valid(self,main_dic):
        dic = {"Date-to(dd-mm-yyyy)":int,"Frequency":int,"Employee-id":int,"Title":str,"Description":"both","Property-id":int,"Priority":int,"Suggested-contractor":str}
        for key in dic.keys():
            if dic[key] == str:
                get_validation = main_dic[key].replace(" ", "").isalpha()
            elif dic[key] == int:
                get_validation = main_dic[key].replace("-","").isdigit()
            # to check if the phone number is a valid length    

            if key == "Date-to(dd-mm-yyyy)" and get_validation:
                if len(main_dic[key]) != 10:
                    return False, key
            if key == "Frequency":
                if int(main_dic[key]) == 1 or int(main_dic[key]) == 2:
                    pass
                else:
                    return False,key
                
                
            if get_validation == False:

                    return False, key
        return True, key


    def check_date(self,date):
        date = date.split("-")
        if date[0] == 2 and date[1] == 2 and date[2] == 4:
            if date[0] > 0 and date[0] < 32 and date[1] > 0 and date[1] < 13:
                date_time=datetime(int(date[2]),int(date[1]),int(date[0])).date()
                if date_time > datetime.date(datetime.now()):
                    return True

        return False


    


if __name__ == "__main__":
    x1 = datetime.date(datetime.now())
    date = "20-12-2000".split("-")
    print(len(date))
    # print(date)
    x=datetime(int(date[2]),int(date[1]),int(date[0])).date()
    print(x1,x)
    # print(x)
    print((x1- x).days)
    # print(x.strftime("%B"))

    dic_fromat = {"Date-to(dd-mm-yyyy)":"20-12-2020","Frequency(number of days)":"7","Employee-id":"2","Title":"hani","Description":"hehe","Property-id":"3","Priority":"1","Suggested-contractor":" "}
    # g = MaintenanceLL()
    # g.add_maintenance(dic_fromat,1)
    if ["1"]:
        print("yeah")
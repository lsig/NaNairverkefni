

from models.maintenance import Maintenance
from storage_layer.DLAPI import DlAPI
from logic_layer.EmployeeLL import EmployeeLL
from logic_layer.propertyLL import PropertyLL
from logic_layer.jobLL import JobLL
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
        '''This function add maintenance job to csv files but first the function goes to a another function to 
        check if the inputs from the ui layer is valid if it is not valid both functions returns false and the key 
        that was invalid and it returns true if the the input is valid and a empty string'''
        
        self.boss_loc = self.empLL.get_emp_location(boss_id)
        self.boss_id = boss_id
        curr_date = datetime.date(datetime.now())
        valid_bool,key = self.is_valid(curr_date,main_dic)
        if valid_bool:
            
            emp_name =self.empLL.find_employee_name(main_dic["Employee-id"])
            prop_addr,prop_nr = self.get_property_info(main_dic["Property-id"])
            cont_names = self.get_cont_names(main_dic["Suggested-contractor(id)"]) 
            print(cont_names)# þarf að bæta við þessu í dl
            # bæta við nöfnunum9
            main_job = Maintenance(self.assign_id(),curr_date,main_dic["Date-to(dd-mm-yyyy)"],main_dic["Frequency(Week: 1, or Month: 2)"],emp_name,main_dic["Employee-id"],main_dic["Title"],
            main_dic["Description"],self.boss_loc,prop_addr,prop_nr,main_dic["Property-id"],main_dic["Priority(ASAP; Now; Emergency)"],cont_names,main_dic["Suggested-contractor(id)"].replace(" ",""),"0")
            self.dlapi.add_maintenance_job(main_job)
            return True,key
        return False,key


    def assign_id(self):
        ''' This function finds a new id that is unique to add to a new maintenance job and returns new unique id 
        '''
        all_main_job = self.dlapi.get_maintenance_jobs()
        if all_main_job != []:
            new_id = int(all_main_job[len(all_main_job)-1]["id"])+1
            return str(new_id)
        return str(1)

    def is_valid(self,today,main_dic):
        ''' This function validates the input, checks if the if the id exists and it is in the same 
        location as the boss that created the job and checks if the date and frequency is valid. This function 
        returns false if the input is invalid and the key that is invalid, it returns true if all the input is correct
        and an empty string
        '''
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
                if emp_dic == None or emp_dic["Destination"] != self.boss_loc :
                    return False,key

            if key == "Property-id" and get_validation:
                prop_dic = self.get_property(main_dic[key])
                if prop_dic == {} or prop_dic["Destination"] != self.boss_loc:
                    return False,key
            if key == "Suggested-contractor(id)"  and main_dic[key] != "":
                get_validation = main_dic[key].replace(",","").replace(" ","").isdigit()
                if get_validation == False:
                    return False,key
                cont_booL = self.check_cont_dic(main_dic[key].replace(" ", ""))
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
        if   date_time != 0 and (date_time-today).days <= freq:
                return False,"Date-to(dd-mm-yyyy)"
        return True,"" 


    def check_date(self,date):
        ''' this function takes the date checks if the input date is valid. It is used by isvalid() and returns false if the 
        date is invalid and returns the date in datetime if the date is valid  
        '''
        if len(date[0]) == 2 and len(date[1]) == 2 and len(date[2]) == 4:
            if int(date[1]) > 0 and int(date[1]) < 13:
                nr_days_in_months=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if 0 < int(date[0]) <= nr_days_in_months[int(date[1])-1]:
                    date_time=datetime(int(date[2]),int(date[1]),int(date[0])).date()
                    if date_time > datetime.date(datetime.now()):
                        return date_time
        return False


    def find_emp(self,id):
        ''' this function used a function in EmployeeLL to find a the employee by his id and return a dict of
        his info and returns false if the id is invalid, none if there is no employee with that id and 
        the dict of the employee if the exist and is a valid id
        '''
        return self.empLL.find_emp_id(id,self.dlapi.get_all_emp())

    def get_property(self,id):
        ''' this function used a function in PropertyLL to find a the property by it's id and return a dict of
        his info and returns false if the id is invalid, none if there is no property with that id and 
        the dict of the property if the exist and is a valid id
        '''
        return self.propLL.find_prop_id(id,self.dlapi.get_property_info())

    def check_cont_dic(self,id):
        ''' this function checks if the location of the contractor is the same as the location of the boss 
        that is creating the maintenance job retrun false if they are not in the same location and true other
        wise
        '''
        all_cont = self.dlapi.get_all_cont()
        for dic in all_cont:
            if dic["id"] == id:
                if dic["Location"] == self.boss_loc:
                        return True
                else:
                    return False     
        return False        
        


    def get_cont_names(self,cont_id):
        ''' this functions find the name of the contractor by his id and returns his name if there is 
        no contractor the this function returns a empty string
        '''
        if cont_id != "":
            all_conts_lis = self.dlapi.get_all_cont()
            for dic in all_conts_lis:
                if dic["id"] == cont_id:
                   return dic["Name"]
        return ""


    def get_property_info(self,prop_id):
        ''' this function finds the property address and Property-number by it's id and returns
         it's address and Property-number if the id exists and two empty strings if the id does not exist
        '''
        prop_dic = self.get_property(prop_id)
        if prop_id != {}:
            return prop_dic["Address"],prop_dic["Property-number"]
        return " "," "

    def get_all_main_jobs(self):
        ''' this functions gets all the maintenance jobs that are in the data files
        '''
        return self.dlapi.get_maintenance_jobs()

    def add_to_job(self):
        ''' This functions add jobs to the job request if the maintenance job was last added job is either 2 days from a week or 
        2 days from a month this functions does this for all maintenance job but it first checks if the 
        maintenance job is expered if the job is expiered this function stops to add to jobs
        '''
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
        ''' this functions check if the maintenance job is expiered or not. if the job is expiered this function
        changes the status to 1 
        '''
        counter = 0
        for main_dic in all_main_jobs:
            if main_dic["Date-to"] != "":
                date_lis = main_dic["Date-to"].split("-")
                date=datetime(int(date_lis[2]),int(date_lis[1]),int(date_lis[0])).date()
                today = datetime.date(datetime.now())
                if (date-today).days < 0:
                    main_dic["Status"] = "1"
                    all_main_jobs[counter] = main_dic
            counter += 1
        self.update_main_job(all_main_jobs)
        
        
    def update_main_job(self,all_main_jobs):
        self.dlapi.change_maintenance_job(all_main_jobs)
        
    # þarf að bæta við search by sting 
if __name__ == "__main__":
    x1 = datetime.date(datetime.now())
    print(x1)
    if x1 != 0:
        print("w")
    # print(x1)
    # date = "20-12-2000".split("-")
    # print(len(date))
    # # print(date)
    # x=datetime(int(date[2]),int(date[1]),int(date[0])).date()
    # print(x1>x)
    # # print(x)
    # print((x1- x).days)
    # print(x.strftime("%B"))

    dic_fromat = {"Date-to(dd-mm-yyyy)":"21-12-2021","Frequency(Week: 1, or Month: 2)":"1","Employee-id":"5","Title":"hani","Description":"hehe","Property-id":"2","Priority(ASAP; Now; Emergency)":"Asap","Suggested-contractor(id)":"2"}
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
    # g.add_to_job()
    print("-2".isdigit())
    # print(g.get_all_main_jobs())
    # g.update_main_job(DlAPI.get_maintenance_jobs())
    # x1 = datetime.date(datetime.now())
    # x2 = x1+ timedelta(days=10)
    # print(x1,x2)
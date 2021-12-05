from storage_layer.DLAPI import DlAPI
from models.job import Job
from datetime import datetime

class JobLL:
    def __init__(self,id):
        self.dlapi = DlAPI()
        self.boss_loc = self.get_emp_location(id)
    
    def add_job(self,job_dic):
        if self.is_valid(job_dic):
            auto_id = self.assign_id_job()
            cur_date = datetime.date(datetime.now())
            emp_name = self.find_employee_name(job_dic["Employee-id"])
            job = Job(auto_id,cur_date,emp_name,job_dic["Employee-id"],job_dic["Title"],job_dic["Description"],self.boss_loc,self.prop_address_from_id(job_dic["Property-id"])[0],self.prop_address_from_id(job_dic["Property-id"])[1],job_dic["Property-id"],job_dic["Priority"],job_dic["Suggested-contractors"],"0")
            self.dlapi.add_job(job)
            return True
        return False

    def assign_id_job(self):
        all_job_lis = self.dlapi.get_jobs()
        if all_job_lis == []:
            new_id = 1
        else:
            new_id = int(all_job_lis[len(all_job_lis)-1]["id"])+1
        return str(new_id)
    
    def find_employee_name(self,id):
        employee_names = self.dlapi.get_all_emp()
        for dic in employee_names:
            if int(id) == int(dic["id"]):
                emp_name = dic["Name"]
        return emp_name

    def get_emp_location(self,id):
        emp_lis = self.dlapi.get_all_emp()
        for dic in emp_lis:
            if int(id) == int(dic["id"]):
                boss_location = dic["Destination"]
        return boss_location
        
        #big validation check
    def is_valid(self,job_dic) -> bool:
        dic = {"Employee-id":int, "Title":"both", "Description":"both", "Property-id":int,"Priority":int,"Suggested-contractors":int}
        for key in dic.keys():
            if dic[key] == str and dic[key] != "both":
                get_validation = job_dic[key].replace(" ", "").isalpha()
            elif dic[key] == int and dic[key] != "both":
                get_validation = job_dic[key].replace("-","").isdigit()
                if key == "Employee-id":
                    if self.boss_loc != self.get_emp_location(job_dic["Employee-id"]):
                        return False
                if key == "Property-id":
                    if self.prop_address_from_id(job_dic["Property-id"])[2] != self.boss_loc:
                        return False
                if key == "Priority":
                    if int(job_dic[key]) <= 0 or int(job_dic[key]) > 3:
                        return False
                    else:
                        job_dic[key] = self.priority_word(job_dic[key])
            # to check if address or property number are empty    
            if dic[key] == "both":
                if job_dic[key] == "":
                    return False
            #check if Destination is within bounds
            if get_validation == False:

                    return False
        return True


    def prop_address_from_id(self,id):
        addresses = self.dlapi.get_property_info()
        for dic in addresses:
            if int(id) == int(dic["id"]):
                prop_info = [dic["Address"],dic["Property-number"],dic["Destination"]]
        return prop_info

    def priority_word(self,prior):
        priority = ["ASAP","Now","Emergancy"]
        ret_val = priority[int(prior)-1]
        return ret_val

    def find_jobs_by_str(self,user_string,job_lis,key):
        ret_lis=[]
        if user_string.replace(" ",""):
            for dic in job_lis:
                if user_string.lower() in dic[key].lower():
                    ret_lis.append(dic)
            return ret_lis
        return False


    
    def get_all_jobs(self):
        all_jobs = self.dlapi.get_jobs()
        return all_jobs
    


if __name__ == "__main__":
    g = JobLL("1")
    #print(g.find_employee_name("5"))
    #g.add_job({"Employee-id":"2","Title":"Maxim","Description":"something","Property-id":"1","Priority":"1","Suggested-contractors":"1"})
    #bool2 = g.is_valid({"Employee-id":"2","Title":"something1","Description":"Do something","Property-id":"1","Priority":"1","Suggested-contractors":"1"})
    #print(bool2)
    #print(g.prop_address_from_id("1"))
    print(g.find_jobs_by_str("o",g.get_all_jobs(),"Title"))
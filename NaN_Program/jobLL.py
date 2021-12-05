from storage_layer.DLAPI import DlAPI
from models.job import Job
from datetime import datetime
from propertyLL import PropertyLL

class JobLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.propll = PropertyLL()
    
    def add_job(self,job_dic):
        #if self.is_valid(job_dic):
        #job_dic = self.propll.replace_loc_num_with_name(job_dic)
        job = Job(self.assign_id_job(),datetime.date(datetime.now()),self.find_employee_name(job_dic["Employee-id"]),job_dic["Employee-id"],job_dic["Title"],job_dic["Description"],job_dic["Location"],self.propll.prop_address_from_id(job_dic["Property-id"])[0],self.propll.prop_address_from_id(job_dic["Property-id"])[1],job_dic["Property-id"],job_dic["Priority"],job_dic["Suggested-contractors"],"0")
        self.dlapi.add_job(job)
        return True
        #return False

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
            if id in dic["id"]:
                emp_name = dic["Name"]
        return emp_name



if __name__ == "__main__":
    g = JobLL()
    #print(g.find_employee_name("5"))
    g.add_job({"Employee-id":"7","Title":"something","Description":"Do something","Location":"1","Property-id":"10","Priority":"HIGH","Suggested-contractors":"thomas the tank engine"})
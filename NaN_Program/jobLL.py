from storage_layer.DLAPI import DlAPI
from models.job import Job
from datetime import datetime
from EmployeeLL import EmployeeLL
#change job will require self.boss fetching!!!!!!!!!!!!!!!!!!!!! note to self
class JobLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empLL = EmployeeLL()
        self.boss_loc = ""
    
    def add_job(self,job_dic,id,main_job_bool=False):

        if main_job_bool == False:
            self.id = id
            self.boss_loc = self.empLL.get_emp_location(id)
            job_dic["Type"] = ''
            valid, key = self.is_valid(job_dic)
            if valid:
                cur_date = datetime.date(datetime.now())
                type = "Regular job"
                emp_name = self.empLL.find_employee_name(job_dic["Employee-id"])
                if job_dic["Suggested-contractor(id)"] != '':
                    con_name = self.get_con_name_and_location(job_dic["Suggested-contractor(id)"])["Name"]
                else:
                    con_name = ''
                prop_addr,prop_nr, prop_loc = self.prop_address_from_id(job_dic["Property-id"])
            else:
                return False,key

        else:
            cur_date = job_dic["Date-created"]
            type = "Maintenace job"
            emp_name = job_dic["Employee"]
            con_name = job_dic["Suggested-contractor"]
            self.boss_loc = job_dic["Location"]
            prop_nr = job_dic["Property-number"]
            prop_addr = job_dic["Property"]

        auto_id = self.assign_id_job()
        job = Job(auto_id,cur_date,emp_name,job_dic["Employee-id"],job_dic["Title"],job_dic["Description"],self.boss_loc,prop_addr,prop_nr,job_dic["Property-id"],job_dic["Priority(ASAP; Now; Emergency)"],job_dic["Suggested-contractor(id)"],con_name,"0",type)
        self.dlapi.add_job(job)
        return True, None

    def assign_id_job(self):
        all_job_lis = self.dlapi.get_jobs()
        if all_job_lis == []:
            new_id = 1
        else:
            new_id = int(all_job_lis[len(all_job_lis)-1]["id"])+1
        return str(new_id)
    
    # def find_employee_name(self,id):
    #     employee_names = self.dlapi.get_all_emp()
    #     for dic in employee_names:
    #         if int(id) == int(dic["id"]):
    #             emp_name = dic["Name"]
    #     return emp_name

    # def get_emp_location(self,id):
    #     emp_lis = self.dlapi.get_all_emp()
    #     for dic in emp_lis:
    #         if int(id) == int(dic["id"]):
    #             boss_location = dic["Destination"]
    #             return boss_location
    #     none_val = "None"
    #     return none_val
        
        #big validation check
    def is_valid(self,job_dic) -> bool:
        priority_check = False
        dic = {"Employee-id":int, "Title":"both", "Description":"both", "Property-id":int,"Priority(ASAP; Now; Emergency)":str,"Suggested-contractor(id)":int}
        for key in dic.keys():
            if dic[key] == str and dic[key] != "both":
                get_validation = job_dic[key].replace(" ", "").isalpha()
                if key == "Priority(ASAP; Now; Emergency)":
                    for row in self.priority_word_check():
                        if job_dic["Priority(ASAP; Now; Emergency)"].lower() == row.lower():
                            priority_check = True
                            job_dic["Priority(ASAP; Now; Emergency)"] = row
                    if priority_check == False:
                        return False, key
            elif dic[key] == int and dic[key] != "both":
                if job_dic[key] == "" and key != "Suggested-contractor(id)":
                    return False,key
                if key != "Suggested-contractor(id)":    
                    get_validation = job_dic[key].replace("-","").isdigit()
                if key == "Employee-id" and get_validation:
                    if self.boss_loc != self.empLL.get_emp_location(job_dic["Employee-id"]):
                        return False,key
                    if job_dic["Type"] == "":
                        if self.id == job_dic["Employee-id"]:
                            return False,key
                if key == "Property-id" and get_validation:
                        if self.prop_address_from_id(job_dic["Property-id"])[2] != self.boss_loc:
                            return False,key
                if key == "Suggested-contractor(id)" and get_validation:
                    if job_dic["Suggested-contractor(id)"] != '':
                        if self.boss_loc != self.get_con_name_and_location(job_dic[key])["Location"]:
                            return False,key
                    else:
                        job_dic["Suggested-contractor(id)"] = ''
            # to check if address or property number are empty    
            if dic[key] == "both":
                if job_dic[key] == "":
                    return False,key
            #check if Destination is within bounds
            if get_validation == False:
                    return False,key
        return True, None


    def prop_address_from_id(self,id):
        addresses = self.dlapi.get_property_info()
        for dic in addresses:
            if int(id) == int(dic["id"]):
                return  [dic["Address"],dic["Property-number"],dic["Destination"]]
        return "","",""

    def priority_word_check(self):
        priority = ["ASAP","Now","Emergency"]
        return priority
   

    def find_jobs_by_str(self,user_string,job_lis,key):
        ret_lis=[]
        if user_string.replace(" ",""):
            for dic in job_lis:
                if user_string.lower() in dic[key].lower():
                    ret_lis.append(dic)
            return ret_lis
        return False


    
    def get_all_jobs(self):
        return self.dlapi.get_jobs()


    def get_all_jobs_sorted(self):#Kristofer!
        all_jobs = self.get_all_jobs()
        jobs_list = self.sort_by_priority(all_jobs)
        jobs_list = self.sort_all_jobs(jobs_list)
        #counter = 0
        #for row in all_jobs:#changes contractor id into name
        #    all_jobs[counter]["Suggested-contractors"] = self.get_con_name_and_location(row["Suggested-contractors"])["Name"]
        #    counter += 1
        return jobs_list
    
    def sort_all_jobs(self, job_list):
        ready_jobs = []
        unready_jobs = []
        finished_jobs = []
        for job in job_list:
            if job['Status'] == '0':
                unready_jobs.append(job) 
            elif job['Status'] == '1':
                ready_jobs.append(job)
            elif job['Status'] == '2':
                finished_jobs.append(job)
        
        return [ready_jobs, unready_jobs, finished_jobs]
    
    def sort_by_priority(self, oldlist):
        new_list = []
        for priority in ['emergency', 'now', 'asap']:
            for job in oldlist:
                if job['Priority(ASAP; Now; Emergency)'].lower() == priority:
                    new_list.append(job)

        for job in oldlist:
            if job not in new_list:
                new_list.append(job)

        return new_list

    
    def total_jobs_count(self):
        return len(self.dlapi.get_jobs())



    def get_con_name_and_location(self,id):#fer líklegast í contractorLL
        con_list = self.dlapi.get_all_cont()
        for dic in con_list:
            if int(id) == int(dic["id"]):
                con_info = {"Name":dic["Name"],"Location":dic["Location"]}
                return con_info        
        con_info = {"Name":"null","Location":"null"}
        return con_info 
        

    def edit_info(self,edit_job_dic,id): #virkar ekki find id location virkar ekki
        self.boss_loc = edit_job_dic["Location"]
        valid, key = self.is_valid(edit_job_dic)
        if valid:
            all_lis_job = self.dlapi.get_jobs()
            dic = self.find_job_id(edit_job_dic["id"],all_lis_job)
            job_loc_in_lis = self.find_id_location_job(dic,all_lis_job)
            all_lis_job[job_loc_in_lis]= edit_job_dic
            self.dlapi.change_job(all_lis_job)
            return True,None
        return False,key

    def find_job_id(self,id,all_job_lis):
        if id.isdigit():
            for dic in all_job_lis:
                if int(dic["id"]) == int(id):
                    dic = dic
                    return dic 
            return None #[{"Text":"No employee with this id"}]
        return False


    def find_id_location_job(self,dic,all_lis_job):
        for i in range(len(all_lis_job)):
            if dic == all_lis_job[i]:
                return i




    def search_time_period(self,time_period_from,time_period_to,all_job_lis=None):
        # all_job_lis = self.get_all_jobs()
        if self.check_date(time_period_from) and self.check_date(time_period_to):
            time_period_from = time_period_from.split("-")
            time_period_to = time_period_to.split("-")
            date_from = datetime(int(time_period_from[2]),int(time_period_from[1]),int(time_period_from[0])).date()
            date_to = datetime(int(time_period_to[2]),int(time_period_to[1]),int(time_period_to[0])).date()
            #print(date_from,date_to)
            if date_from <= date_to:
                ret_lis = []
                for dic in all_job_lis:
                    job_date_lis = dic["Date-created"].split("-")
                    job_date = datetime(int(job_date_lis[0]),int(job_date_lis[1]),int(job_date_lis[2])).date()
                    if date_from <= job_date and date_to >= job_date:
                        ret_lis.append(dic)
                if ret_lis != []:
                    return ret_lis
        return False


    def check_date(self,date):
        ## dd-mm-yyyy or 
        if date.replace("-","").isdigit():
            date = date.split("-")
            if len(date) == 3:
                if len(date[0]) == 2 and len(date[1]) == 2 and len(date[2]) == 4:
                    if int(date[1]) > 0 and int(date[1]) < 13:
                        nr_days_in_months=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                        if 0 < int(date[0]) <= nr_days_in_months[int(date[1])-1]:
                            return True
        return False

                








if __name__ == "__main__":
    g = JobLL()
    (g.get_all_jobs_sorted())
    #print(g.find_employee_name("5"))
    print(g.add_job({"Employee-id":"2","Title":"Maxim","Description":"something","Property-id":"1","Priority(ASAP; Now; Emergency)":"Asap","Suggested-contractor(id)":"1","Suggested-contractors":"1"},"1"))
    #bool2 = g.is_valid({"Employee-id":"2","Title":"something1","Description":"Do something","Property-id":"1","Priority":"1","Suggested-contractors":"1"})
    #print(bool2)
    #print(g.prop_address_from_id("1"))
    #print(g.find_jobs_by_str("o",g.get_all_jobs(),"Title"))
    #print(g.get_con_name_and_location("1")["Name"])
    #g.edit_info({"id":"1","Date-created":"2021-12-05","Employee":"Jan Jacobsen","Employee-id":"1","Title":"small window clean","Description":"cleandd the windows!","Location":"Longyearbyen","Property":"Vei 217","Property-number":"F959594","Property-id":"1","Priority":"1","Suggested-contractors":"1","Status":"0"},"1")
    #print(g.get_all_jobs())

    date_1 = datetime(4441,10,13).date()
    date_2 = datetime(2021,12,10).date()
    print(date_1,date_2)
    date_3 = datetime.date(datetime.now())
    if date_1 <= date_3 and date_2 >= date_3:
        print(len("2222-22-22"))

    print("09-22-2012".split("-"),len(""),int("-09"))
    # str_test = "2222-10-10"
    # datetime.strptime(str_test,'%y-%m-%d') 
    print(datetime(4441,10,13))
    print(g.search_time_period("28-02-2021","11-12-2021"))



    
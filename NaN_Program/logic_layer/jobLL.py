from storage_layer.DLAPI import DlAPI
from models.job import Job
from datetime import datetime
from logic_layer.EmployeeLL import EmployeeLL
#change job will require self.boss fetching!!!!!!!!!!!!!!!!!!!!! note to self
class JobLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empLL = EmployeeLL()
        self.boss_loc = ""
    #Add job, Ignores validation if regular maintenance is using this class
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
            #Getting information from regular_maintenance
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

#Auto incremented id
    def assign_id_job(self):
        all_job_lis = self.dlapi.get_jobs()
        if all_job_lis == []:
            new_id = 1
        else:
            new_id = int(all_job_lis[len(all_job_lis)-1]["id"])+1
        return str(new_id)
    

        
        #Validation check makes sure that property, employee and contractor is located in the same location/destination
        #Also checks for incorrect input
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
                if key == "Suggested-contractor(id)" and get_validation: #Contractor can be empty string
                    if job_dic["Suggested-contractor(id)"] != '':
                        if self.boss_loc != self.get_con_name_and_location(job_dic[key])["Location"]:
                            return False,key
                    else:
                        job_dic["Suggested-contractor(id)"] = '' 
            if dic[key] == "both":
                if job_dic[key] == "":
                    return False,key
            if get_validation == False:
                    return False,key
        return True, None

#getting property address and destination
    def prop_address_from_id(self,id):
        addresses = self.dlapi.get_property_info()
        for dic in addresses:
            if int(id) == int(dic["id"]):
                return  [dic["Address"],dic["Property-number"],dic["Destination"]]
        return "","",""
#Three allowed priority words
    def priority_word_check(self):
        priority = ["ASAP","Now","Emergency"]
        return priority
   
#Search engine that searches by string
    def find_jobs_by_str(self,user_string,job_lis,key):
        ret_lis=[]
        if user_string.replace(" ",""):
            for dic in job_lis:
                if user_string.lower() in dic[key].lower():
                    ret_lis.append(dic)
            return ret_lis
        return False


#Returns all jobs list of dictrionaries
    def get_all_jobs(self):
        return self.dlapi.get_jobs()

#sorts all jobs for ui
    def get_all_jobs_sorted(self):#Kristofer!
        all_jobs = self.get_all_jobs()
        jobs_list = self.sort_by_priority(all_jobs)
        jobs_list = self.sort_all_jobs(jobs_list)
        #counter = 0
        #for row in all_jobs:#changes contractor id into name
        #    all_jobs[counter]["Suggested-contractors"] = self.get_con_name_and_location(row["Suggested-contractors"])["Name"]
        #    counter += 1
        return jobs_list
#sorts jobs by status
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
    
#sort by priority for ui
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

#Return total number of jobs for avg rating    
    def total_jobs_count(self):
        return len(self.dlapi.get_jobs())


#For validation. get Contractor name and location
    def get_con_name_and_location(self,id):#fer líklegast í contractorLL
        con_list = self.dlapi.get_all_cont()
        for dic in con_list:
            if int(id) == int(dic["id"]):
                con_info = {"Name":dic["Name"],"Location":dic["Location"]}
                return con_info        
        con_info = {"Name":"null","Location":"null"}
        return con_info 
        
#this functiion replaces one line from a list, for edit
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
#Returns dictionary for job with specific id
    def find_job_id(self,id,all_job_lis):
        if id.isdigit():
            for dic in all_job_lis:
                if int(dic["id"]) == int(id):
                    dic = dic
                    return dic 
            return None #[{"Text":"No employee with this id"}]
        return False

#find index in list for edit
    def find_id_location_job(self,dic,all_lis_job):
        for i in range(len(all_lis_job)):
            if dic == all_lis_job[i]:
                return i




    def search_time_period(self,time_period_from,time_period_to,all_job_lis=None):
        ''' this functions searches for all job or reports for a specific time period it first checks if the dates
        are valid and then if the end of time period is bigger or equals to the start of the time period if and then if
        it is a report or a job. it returns false if the dates are invalid or there are no jobs or reports at that
        time period other wise it returns a list of all the jobs or reports at that time period
        '''
        if self.check_date(time_period_from) and self.check_date(time_period_to):
            time_period_from = time_period_from.split("-")
            time_period_to = time_period_to.split("-")
            date_from = datetime(int(time_period_from[2]),int(time_period_from[1]),int(time_period_from[0])).date()
            date_to = datetime(int(time_period_to[2]),int(time_period_to[1]),int(time_period_to[0])).date()
            #print(date_from,date_to)
            if date_from <= date_to:
                ret_lis = []
                for dic in all_job_lis:
                    if "Date-created" in dic.keys():
                        job_date_lis = dic["Date-created"].split("-")
                    elif "Date" in dic.key.keys():
                        job_date_lis = dic["Date"].split("-")

                    job_date = datetime(int(job_date_lis[0]),int(job_date_lis[1]),int(job_date_lis[2])).date()
                    if date_from <= job_date and date_to >= job_date:
                        ret_lis.append(dic)
                if ret_lis != []:
                    return ret_lis
        return False


    def check_date(self,date):
        ''' this functions checks if the date are valid from date time and it returns false if the the date is not valid
        other wise true
        '''
        if date.replace("-","").isdigit():
            date = date.split("-")
            if len(date) == 3:
                if len(date[0]) == 2 and len(date[1]) == 2 and len(date[2]) == 4:
                    if int(date[1]) > 0 and int(date[1]) < 13:
                        nr_days_in_months=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                        if 0 < int(date[0]) <= nr_days_in_months[int(date[1])-1]:
                            return True
        return False

                









    

from os import name
from contractorLL import ContractorLL
from propertyLL import PropertyLL
from jobLL import JobLL
from EmployeeLL import EmployeeLL
from locationLL import LocationLL
from reportsLL import ReportsLL
from maintenanceLL import MaintenanceLL

class LLAPI:
    def __init__(self):
        self.id = id
        self.contLL = ContractorLL()
        self.propLL = PropertyLL()
        self.jLL = JobLL()
        self.empll = EmployeeLL()
        self.locLL = LocationLL()
        self.repLL = ReportsLL()
        self.maintLL = MaintenanceLL()


    #ContractorLL
    def add_cont(self,con_lis,loc):
        return self.contLL.add_contractor(con_lis,loc)

    def list_all_contractors(self):
        return self.contLL.lis_all_cont()
    
    def search_contractor(self, userstring, con_list, key):
        return self.contLL.find_con_by_str(userstring, con_list, key)
    
    def filter_contr_id(self, input, contr_list):
        return self.contLL.find_con_id(input, contr_list)
    
    def edit_contractor(self, contrdict):
        return self.contLL.edit_info(contrdict)


    #PropertyLL
    def add_prop(self,prop_lis):
        return self.propLL.add_property(prop_lis)

    def get_prop_info(self):
        return self.propLL.get_all_prop()
    
    def all_prop_lis(self):
        return self.propLL.get_all_prop_lis()

    def filter_property_id(self,id,prop_lis):
        return self.propLL.find_prop_id(id,prop_lis)
    
    def edit_prop(self, propdict):
        return self.propLL.edit_info(propdict)
    
    def search_property(self, string, propertylist, key):
        return self.propLL.find_prop_by_str(string, propertylist, key)
    

    #EmployeeLL
    def get_emp_info(self):
        return self.empll.list_all_employees()

    def add_emp(self, emp_lis):
        return self.empll.add_employee(emp_lis)

    def edit_emp(self, emp_dic):
        return self.empll.edit_employee(emp_dic)

    def filter_employee_id(self, id, emp_lis):
        return self.empll.find_emp_id(id, emp_lis)

    def login_information(self,email):
        return self.empll.login_info(email)
    
    def search_employee(self, string, employeelist, key):
        return self.empll.find_emp_by_str(string, employeelist,key)


    #LocationLL
    def search_destination(self,string, destinationlist, key):
        return self.locLL.find_dest_by_str(string, destinationlist, key)
    
    def get_dest_info(self):
        return self.locLL.list_all_loc()

    def filter_loc_id(self,id,loc_lis):
        return self.locLL.find_loc_id(id,loc_lis)

    def edit_loc(self,loc_dic):
        return self.locLL.edit_info(loc_dic)
    
    def add_loc(self, loc_dic):
        return self.locLL.add_location(loc_dic)


    #ReportLL
    def get_report_info(self):
        return self.repLL.get_all_rep()
    
    def search_report(self,string, reportlist, key):
        return self.repLL.find_rep_by_str(string, reportlist, key)
    
    def filter_rep_id(self,id,rep_lis):
        return self.repLL.find_rep_id(id,rep_lis)
    def edit_rep(self,rep_dict):
        return self.repLL.edit_report_info(rep_dict)
    
    def get_sorted_reports(self):
        return self.repLL.sort_all_reports()


    #JobLL
    def add_job(self,job_lis,id):
        return self.jLL.add_job(job_lis,id)

    def get_job(self):
       return self.jLL.get_all_jobs()
    
    def get_sorted_jobs(self):
        return self.jLL.get_all_jobs_sorted()
    
    def count_jobs(self):
        return self.jLL.total_jobs_count()
    
    def filter_job_id(self, idstring, job_list):
        return self.jLL.find_job_id(idstring, job_list)
    
    def search_job(self,string, joblist, key):
        return self.jLL.find_jobs_by_str(string, joblist, key)

    
    #MaintenanceLL
    def get_all_maint_jobs(self):
        return self.maintLL.get_all_main_jobs()
    

        

if __name__ == "__main__":
    g = LLAPI()
    #g.add_cont(["John nohands","Elton john","3549990000","00","Tórshavn"])
    #print(g.all_prop_lis)
    
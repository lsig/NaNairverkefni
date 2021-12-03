from storage_layer.employeeDL import EmployeeDL
from storage_layer.locationDL import LocationDL
from storage_layer.propertyDL import PropertyDL
from storage_layer.contractorDL import ContractorDL
from storage_layer.jobDL import JobDL
from storage_layer.reportDL import ReportDL
from storage_layer.maintenanceDL import MaintenanceDL



class DlAPI:
    def __init__(self):
        self.empDL = EmployeeDL() 
        self.locDL = LocationDL() 
        self.propDL = PropertyDL() 
        self.contDL = ContractorDL() 
        self.reportDL = ReportDL()
        self.jobDL = JobDL() 
        self.maintenjobDL = MaintenanceDL()


    def get_all_emp(self):
        return self.empDL.get_all_employee()

    def add_emp(self,emp):
        self.empDL.add_employee(emp)

    def change_emp_info(self,all_emp_lis):
        self.empDL.change_emp_info(all_emp_lis)

    def get_loc_info(self):
        return self.locDL.get_all_loc()

    def add_loc(self,loc):
        self.locDL.add_loc(loc)

    def change_loc_info(self,all_loc_lis):
        self.locDL.change_loc_info(all_loc_lis)

    def get_property_info(self):
        return self.propDL.get_all_property() 

    def add_property(self,prop_lis):
        self.propDL.add_property(prop_lis) 

    def change_property_info(self,all_prop_lis):
        self.propDL.change_prop_info(all_prop_lis) 

    def get_all_cont(self):
        return self.contDL.get_all_contractor() 

    def add_cont(self,con_lis):
        self.contDL.add_contractor(con_lis)

    def change_cont(self,all_con_lis):
        self.contDL.change_con_info(all_con_lis)

    def get_all_report(self):
        return self.reportDL.get_all_reports()

    def add_report(self,report):
        self.reportDL.add_report(report)

    def change_report(self,all_report_lis):
        self.reportDL.change_report_info(all_report_lis)

    def get_jobs(self):
        return self.jobDL.get_all_jobs()  

    def add_job(self,job):
        self.jobDL.add_job(job) 

    def change_job(self,jobs):
        self.jobDL.change_job_info(jobs) 

    def get_maintenance_jobs(self):
        return self.maintenjobDL.get_all_maintenance_jobs()

    def add_maintenance_job(self,main_job):
        self.maintenjobDL.add_maintenance_job()

    def change_maintenance_job(self,all_main_jobs_lis):
        self.maintenjobDL.change_maintenance_job_info(all_main_jobs_lis)


    




        


if __name__ == "__main__":
    d = DlAPI()
    # print(d.get_all_emp())
    # emp = Employee("10","siggi","0","Traðartún 3; 108; Argir; Faroe Islands","6666666","6666667","siggi@Nanair.is","Tórshavn","0")
    # d.add_emp(emp)

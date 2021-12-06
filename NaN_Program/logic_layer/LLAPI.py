
from os import name
from contractorLL import ContractorLL
from propertyLL import PropertyLL
from jobLL import JobLL
from EmployeeLL import EmployeeLL

class LLAPI:
    def __init__(self):
        self.id = id
        self.contLL = ContractorLL()
        self.propLL = PropertyLL()
        self.jLL = JobLL()
        self.empll = EmployeeLL()


    def add_cont(self,con_lis):
        return self.contLL.add_contractor(con_lis)

    def add_prop(self,prop_lis):
        return self.propLL.add_property(prop_lis)

    def get_prop_info(self):
        return self.propLL.get_all_prop()
    
    def all_prop_lis(self):
        return self.propLL.get_all_prop_lis()


    def filter_property_id(self,id,prop_lis):
        return self.propLL.find_prop_id(id,prop_lis)

    def add_job(self,job_lis,id):
        self.jLL.add_job(job_lis,id)
    
    def edit_prop(self, propdict):
        self.propLL.edit_info(propdict)

    def get_emp_info(self):
        return self.empll.list_all_employees()

    def add_emp(self, emp_lis):
        return self.empll.add_employee(emp_lis)

    def edit_emp(self, emp_dic):
        self.empll.edit_employee(emp_dic)

    def filter_employee_id(self, id, emp_lis):
        return self.empll.find_emp_id(id, emp_lis)

    
    

        

if __name__ == "__main__":
    g = LLAPI()
    #g.add_cont(["John nohands","Elton john","3549990000","00","Tórshavn"])
    #print(g.all_prop_lis)
    
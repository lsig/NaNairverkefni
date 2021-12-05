
from os import name
from contractorLL import ContractorLL
from propertyLL import PropertyLL
from jobLL import JobLL
class LLAPI:
    def __init__(self):
        self.contLL = ContractorLL()
        self.propLL = PropertyLL()
        self.jLL = JobLL()


    def add_cont(self,con_lis):
        self.contLL.add_contractor(con_lis)

    def add_prop(self,prop_lis):
        self.propLL.add_property(prop_lis)

    def get_prop_info(self):
        return self.propLL.get_all_prop()
    
    def all_prop_lis(self):
        return self.propLL.get_all_prop_lis()


    def filter_property_id(self,id):
        return self.propLL.find_prop_id(id)

    def add_job(self,job_lis):
        self.jLL.add_job(job_lis)

        

if __name__ == "__main__":
    g = LLAPI()
    #g.add_cont(["John nohands","Elton john","3549990000","00","Tórshavn"])
    #print(g.all_prop_lis)
    
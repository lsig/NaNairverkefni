
from os import name
from contractorLL import ContractorLL
from propertyLL import PropertyLL
class LLAPI:
    def __init__(self):
        self.contLL = ContractorLL()
        self.propLL = PropertyLL()


    def add_cont(self,con_lis):
        self.contLL.add_contractor(con_lis)

    def add_prop(self,prop_lis):
        self.propLL.add_property(prop_lis)

    def all_prop_lis(self):
        self.propLL.get_all_prop_lis()


if __name__ == "__main__":
    g = LLAPI()
    g.add_cont(["John nohands","Elton john","3549990000","00","Tórshavn"])

    
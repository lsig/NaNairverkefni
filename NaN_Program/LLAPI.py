
from os import name
from contractorLL import ContractorLL
class LLAPI:
    def __init__(self):
        self.contLL = ContractorLL()


    def add_cont(self,con_lis):
        self.contLL.add_contractor(con_lis)


if __name__ == "__main__":
    g = LLAPI()
    g.add_cont(["John nohands","Elton john","3549990000","00","Tórshavn"])

    
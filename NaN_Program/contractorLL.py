from storage_layer.DLAPI import DlAPI
from models.contractor import Contractor

class ContractorLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.model_con = Contractor()

    def add_contractor(self,cont_lis):
        cont = self.model_con(self.assign_id_cont,cont_lis[0],cont_lis[1],cont_lis[2],cont_lis[3],cont_lis[4],"NaN")
        self.dlapi.add_cont(cont)

    def assign_id_cont(self):
        all_cont_lis = self.dlapi.get_all_cont()
        new_id = int(all_cont_lis[len(all_cont_lis)-1]["id"])+1
        return str(new_id)
        
        


if __name__ == "__main__":
    g = ContractorLL()
    # g.add_contractor(["2","John nohands","Elton john","3549990000","00","Tórshavn","8"])
    # g.assign_id_cont()
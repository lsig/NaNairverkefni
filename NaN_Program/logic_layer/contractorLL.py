from storage_layer.DLAPI import DlAPI
from models.contractor import Contractor

class ContractorLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_contractor(self,cont_lis):
        if self.is_valid(cont_lis):
            cont = Contractor(self.assign_id_cont(),cont_lis[0],cont_lis[1],cont_lis[2],cont_lis[3],cont_lis[4],None)
            self.dlapi.add_cont(cont)
            return True
        return False

    def assign_id_cont(self):
        all_cont_lis = self.dlapi.get_all_cont()
        new_id = int(all_cont_lis[len(all_cont_lis)-1]["id"])+1
        return new_id

    def is_valid(self,cont_lis) -> bool:
        dic = {"name":str, "cont_name":str, "phone":int, "working_hours":int,"location":str}
        counter = 0
        for key in dic.keys():
            if dic[key] == str:
                get_validation = cont_lis[counter].replace(" ", "").isalpha()
            else:
                get_validation = cont_lis[counter].replace("-","").isdigit()
            # to check if the phone number is a valid length    
            if key.lower() == "phone" and get_validation:
                if len(cont_lis[counter]) < 7 or len(cont_lis[counter]) > 15:
                    return False, key
            if get_validation == False:

                    return False, key
            counter += 1
        return True


    
        
        


if __name__ == "__main__":
    g = ContractorLL()
    g.add_contractor(["John nohands","Elton john","3549990000","00","Tórshavn"])
    # g.assign_id_cont()
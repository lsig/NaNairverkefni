

from storage_layer.DLAPI import DlAPI
from models.contractor import Contractor

class ContractorLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_contractor(self,cont_lis):
        if self.is_valid(cont_lis):
            cont = Contractor(self.assign_id_cont(),cont_lis[0],cont_lis[1],cont_lis[2],cont_lis[3],cont_lis[4],cont_lis[5],None)
            self.dlapi.add_cont(cont)
            return True
        return False

    def assign_id_cont(self):
        all_cont_lis = self.dlapi.get_all_cont()
        new_id = int(all_cont_lis[len(all_cont_lis)-1]["id"])+1
        return new_id

    def is_valid(self,cont_lis) -> bool:
        dic = {"name":str, "cont_name":str,"profession":str, "phone":int, "working_hours":int,"location":str}
        counter = 0
        for key in dic.keys():
            if dic[key] == str:
                get_validation = cont_lis[counter].replace(" ", "").isalpha()
            else:
                get_validation = cont_lis[counter].replace("-","").isdigit()
            # to check if the phone number is a valid length    
            if key.lower() == "phone" and get_validation:
                if len(cont_lis[counter]) < 7 or len(cont_lis[counter]) > 15:
                    return False
            if get_validation == False:

                    return False
            counter += 1
        return True

    
    def find_con_id(self,id):
        if id.isdigit():
            all_cont_lis=self.dlapi.get_all_cont()
            for dic in all_cont_lis:
                if int(dic["id"]) == int(id):
                    return dic 
            return None
        return False

    # def find_name_con(self,name):
    #     if name.
        



if __name__ == "__main__":
    g = ContractorLL()
    # bool_1 = g.add_contractor(["John nohands","Elton john","bulider","35499900","00","Tórshavn"])
    # print(bool_1)
    print(g.find_con_id("5"))


    # def print_lis(lis):
    #     print(lis)

    # print_lis([1,2,34])

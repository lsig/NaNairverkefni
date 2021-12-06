
from storage_layer.DLAPI import DlAPI
from models.contractor import Contractor

class ContractorLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_contractor(self,cont_dic):
        valid, key = self.is_valid(cont_dic)
        if valid:
            cont = Contractor(self.assign_id_cont(),cont_dic["Name"],cont_dic["Contact-name"],cont_dic["Profession"],cont_dic["Phone"],cont_dic["Working-hours"],cont_dic["Location"],None)
            self.dlapi.add_cont(cont)
            return True, key
        return False, key

    def assign_id_cont(self):
        all_cont_lis = self.dlapi.get_all_cont()
        new_id = int(all_cont_lis[len(all_cont_lis)-1]["id"])+1
        return new_id

    def is_valid(self,cont_dic) -> bool:
        dic = {"Name":str, "Contact-name":str,"Profession":str, "Phone":int, "Working-hours":int,"Location":str}
        for key in dic.keys():
            if dic[key] == str:
                get_validation = cont_dic[key].replace(" ", "").isalpha()
            else:
                get_validation = cont_dic[key].replace("-","").isdigit()
            # to check if the phone number is a valid length    
            if key.lower() == "phone" and get_validation:
                if len(cont_dic[key]) < 7 or len(cont_dic[key]) > 15:
                    return False, key
            if get_validation == False:

                    return False, key
        return True, key

    
    def find_con_id(self,id,all_cont_lis):
        if id.isdigit():
            for dic in all_cont_lis:
                if int(dic["id"]) == int(id):
                    return dic 
            return None
        return False

    def find_name_con(self,name,cont_lis):
        ret_lis=[]
        if name.replace(" ","").isalpha():
            for dic in cont_lis:
                if name.lower() in dic["Name"].lower():
                    ret_lis.append(dic)
            return ret_lis
        return False


    def lis_all_cont(self): # þarf að breyta 
        return self.dlapi.get_all_cont()

    def edit_info(self,edit_con_dic):
        if self.is_valid(edit_con_dic):
            all_lis_cont= self.dlapi.get_all_cont()
            dic = self.find_con_id(edit_con_dic["id"],all_lis_cont)
            # print(dic)
 
            con_loc_in_lis = self.find_id_location_con(dic,all_lis_cont)
            all_lis_cont[con_loc_in_lis]= edit_con_dic
            self.dlapi.change_cont(all_lis_cont)
            return True
        return False



    def find_id_location_con(self,dic,all_lis_cont):
        for i in range(len(all_lis_cont)):
            if dic == all_lis_cont[i]:
                return i
            
            


        
        
        



if __name__ == "__main__":
    g = ContractorLL()
    # bool_1 = g.add_contractor(["John nohands","Elton john","bulider","35499900","00","Tórshavn"])
    # print(bool_1)
    # print(g.find_name_con(""))
    # print(g.lis_all_cont())
    # if "sig" in "siggi":
    #     print("12")
    # bool_2=g.edit_info({"4",,,,,"00",,None})
    bool_2=g.edit_info( {"id":"4","Name":"John is not grate", "Contact-name":"Elton john","Profession":"bulider", "Phone":"35499900", "Working-hours":"00","Location":"Tórshavn","Rating(0-10)":None})

    

    # def print_lis(lis):
    #     print(lis)
    # print("".isdigit())
    # print_lis([1,2,34])
    # lis = [1,2,3,4,5,6]
    # print(len(lis))
    # print(lis[1:len(lis)-1])

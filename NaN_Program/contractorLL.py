
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

    
    def find_con_id(self,id,all):
        if id.isdigit():
            all_cont_lis=self.dlapi.get_all_cont()
            for dic in all_cont_lis:
                if int(dic["id"]) == int(id):
                    return dic 
            return None
        return False

    def find_name_con(self,name):
        ret_lis=[]
        if name.replace(" ","").isalpha():
            for dic in self.dlapi.get_all_cont():
                if name.lower() in dic["Name"].lower():
                    ret_lis.append(dic)
            return ret_lis
        return False


    def lis_all_cont(self):
        ret_lis = []
        for dic in self.dlapi.get_all_cont():
            temp_lis = []
            for key in dic:
               temp_lis.append(dic[key])
            ret_lis.append(temp_lis)
        return ret_lis

    def edit_info(self,con_lis):
        if self.is_valid(con_lis[1:len(con_lis)-1]):
            all_lis_cont= self.dlapi.get_all_cont()
            new_dic = {}
            dic = self.find_con_id(con_lis[0])
            print(dic,con_lis)
            counter = 0
            for key in dic:
                new_dic[key] = con_lis[counter]
                counter += 1
            con_loc_in_lis = self.find_id_location_con(dic,all_lis_cont)
            all_lis_cont[con_loc_in_lis]= new_dic
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
    bool_2=g.edit_info(["4","John is hands","Elton john","bulider","35499900","00","Tórshavn",None])

    

    # def print_lis(lis):
    #     print(lis)
    # print("".isdigit())
    # print_lis([1,2,34])
    lis = [1,2,3,4,5,6]
    print(len(lis))
    print(lis[1:len(lis)-1])

from storage_layer.DLAPI import DlAPI
from models.location import Location
from EmployeeLL import EmployeeLL



class LocationLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empLL = EmployeeLL()
        

    def add_location(self,loc_dic):
        #loc_dic["Destination"] = loc_dic["Destination"].capitalize()
        if self.is_valid(loc_dic): #þarf að bæta fancy bounce í ui :)  
            boss_id = self.empLL.assign_id_emp()
            loc = Location(self.assign_id_loc(),loc_dic["Name"],loc_dic["Country"],loc_dic["Airport"],loc_dic["Phone"],loc_dic["Working-hours"],loc_dic["Manager"],boss_id)
            loc_dic["Destination"] = loc_dic["Name"]
            loc_dic["Phone"] = loc_dic["Phone-manager"]
            loc_dic["Name"] = loc_dic["Manager"]
            loc_dic["Manager"] = "1"
            self.empLL.add_employee(loc_dic)
            self.dlapi.add_loc(loc)


    def assign_id_loc(self):
        all_loc_lis = self.dlapi.get_loc_info()
        if all_loc_lis == []:
            new_id = 1
        else:
            new_id = int(all_loc_lis[len(all_loc_lis)-1]["id"])+1
        return str(new_id)

    def is_valid(self,loc_dic):
        dic = {"Name":str, "Country":str, "Airport":str, "Phone":int,"Working-hours":int,"Manager":str,"Phone-manager":int,"GSM":int}
        for key in dic.keys():
            if dic[key] == str:
                get_validation = loc_dic[key].replace(" ", "").isalpha()
            else:
                get_validation = loc_dic[key].replace("-","").isdigit()
            # to check if the phone number is a valid length    
            if key.lower() == "phone" and get_validation or key.lower() == "phone-manager" and get_validation or key.lower() == "gsm" and get_validation:
                if len(loc_dic[key]) < 7 or len(loc_dic[key]) > 15:
                    return False, key
            if get_validation == False:

                    return False, key
        return True, key

    
    def list_all_loc(self):
        all_loc = self.dlapi.get_loc_info()
        return all_loc


    def find_prop_by_str(self,user_string,loc_lis,key):
        ret_lis=[]
        for dic in loc_lis:
            if user_string.lower() in dic[key].lower():
                ret_lis.append(dic)
        if ret_lis == []:
            return False #skoða þetta svo filter drepur ekki forritið
        return ret_lis



if __name__ == "__main__":
    g = LocationLL()
    #g.add_location({"Name":"Nuuk","Country":"Greenland","Airport":"Nan","Phone":"3548988054","Working-hours":"00","Manager":"lala","Manager-id":"5"})
    #d = g.get_all_prop()
    #d = g.find_prop_id("2",g.get_all_prop())
    #print(d[0]["id"])
    #g.edit_info({"id":"31","Destination":"Kulsuk", "Address":"lol", "Size":"2", "Rooms":"3","Type":"biiiig","Property-number":"poom street 2","Extras":"Windows"})
    #print(g.find_prop_by_str("windowss",g.get_all_prop(),"Extras"))
    #print(g.get_all_prop)
    #{"Name":"John"}
    #d=g.get_destination_name()
    #print(d[0].capitalize())
    g.add_location({"Name":"kdsa","Country":"Greenland","Airport":"Nan","Phone":"56789834","Working-hours":"00","Manager":"John Nolegs","Phone-manager":"123456789","Address":"Cool Street","GSM":"123456788","Social Security":"98876532"})
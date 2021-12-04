from storage_layer.DLAPI import DlAPI
from models.property import Property

class PropertyLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_property(self,prop_dic):
        if self.is_valid(prop_dic):
            prop_dic = self.replace_loc_num_with_name(prop_dic)
            prop = Property(self.assign_id_prop(),prop_dic["Destination"],prop_dic["Address"],prop_dic["Size"],prop_dic["Rooms"],prop_dic["Type"],prop_dic["Property-number"],prop_dic["Extras"])
            self.dlapi.add_property(prop)
            return True
        return False

    def assign_id_prop(self):
        all_prop_lis = self.dlapi.get_property_info()
        new_id = int(all_prop_lis[len(all_prop_lis)-1]["id"])+1
        return str(new_id)
    
    def get_destination_count(self):
        all_desti_lis = self.dlapi.get_loc_info()
        desti_count = int(all_desti_lis[len(all_desti_lis)-1]["id"])
        return desti_count

    def replace_loc_num_with_name(self,dic):
        loc_names_lis = self.dlapi.get_loc_info()
        dic["Destination"] = loc_names_lis[int(dic["Destination"])-1]['Name']
        return dic
    
    def is_valid(self,prop_dic) -> bool:
        dic = {"Destination":int, "Address":"both", "Size":int, "Rooms":int,"Type":str,"Property-number":"both","Extras":str}
        counter = 0
        for key in dic.keys():
            if dic[key] == str and dic[key] != "both":
                if key.lower() == "extras": #replace empty string with none for extras
                    if prop_dic[key] == "":
                        prop_dic[key] = "None"
                get_validation = prop_dic[key].replace(" ", "").isalpha()
            elif dic[key] == int and dic[key] != "both":
                get_validation = prop_dic[key].replace("-","").isdigit()
            # to check if address or property number are empty    
            if dic[key] == "both":
                if prop_dic[key] == "":
                    return False
            #check if Destination is within bounds
            if key.lower() == "destination" and get_validation:
                if  int(prop_dic[key]) <= 0 or int(prop_dic[key]) > self.get_destination_count():
                    return False
            if get_validation == False:

                    return False
            counter += 1
        return True

        
    
    def get_all_prop(self):
        all_prop = self.dlapi.get_property_info()
        return all_prop


    def find_prop_id(self,id,all_prop_lis):
        if id.isdigit():
            for dic in all_prop_lis:
                if int(dic["id"]) == int(id):
                    return dic 
            return None
        return False

    def edit_info(self,edit_prop_dic):
        if self.is_valid(edit_prop_dic):
            edit_prop_dic = self.replace_loc_num_with_name(edit_prop_dic)
            all_lis_prop= self.dlapi.get_property_info()
            dic = self.find_prop_id(edit_prop_dic["id"],all_lis_prop)
            con_loc_in_lis = self.find_id_location_prop(dic,all_lis_prop)
            all_lis_prop[con_loc_in_lis]= edit_prop_dic
            self.dlapi.change_property_info(all_lis_prop)
            return True
        return False
    
    def find_id_location_prop(self,dic,all_lis_prop):
        for i in range(len(all_lis_prop)):
            if dic == all_lis_prop[i]:
                return i

    def find_prop_by_str(self,user_string,prop_lis,key):
        ret_lis=[]
        if user_string.replace(" ",""):
            for dic in prop_lis:
                if user_string.lower() in dic[key].lower():
                    ret_lis.append(dic)
            return ret_lis
        return False

if __name__ == "__main__":
    g = PropertyLL()
    #d = g.get_all_prop()
    #print(d)
    #g.edit_info({"id":"33","Destination":"1", "Address":"Heima 2", "Size":"10", "Rooms":"15","Type":"Best","Property-number":"poom street 2","Extras":"Windows"})
    print(g.find_prop_by_str("ud",g.get_all_prop(),"Extras"))

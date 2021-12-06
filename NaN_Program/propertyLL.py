from storage_layer.DLAPI import DlAPI
from models.property import Property
from datetime import datetime

class PropertyLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_property(self,prop_dic):
        valid, key = self.is_valid(prop_dic)
        if valid:
            #prop_dic = self.replace_loc_num_with_name(prop_dic)
            prop_dic["Destination"] = prop_dic["Destination"].capitalize()
            prop = Property(self.assign_id_prop(),prop_dic["Destination"],prop_dic["Address"],prop_dic["Size"],prop_dic["Rooms"],prop_dic["Type"],prop_dic["Property-number"],prop_dic["Extras"])
            self.dlapi.add_property(prop)
            return True, key
        return False, key

    def assign_id_prop(self):
        all_prop_lis = self.dlapi.get_property_info()
        new_id = int(all_prop_lis[len(all_prop_lis)-1]["id"])+1
        return str(new_id)
    
    def get_destination_count(self):
        all_desti_lis = self.dlapi.get_loc_info()
        desti_count = int(all_desti_lis[len(all_desti_lis)-1]["id"])
        return desti_count

        
    def get_destination_name(self):
        desti_names = []
        all_desti_lis = self.dlapi.get_loc_info()
        for row in all_desti_lis:    
            desti_names.append(row["Name"])
        return desti_names

    def replace_loc_num_with_name(self,dic):
        loc_names_lis = self.dlapi.get_loc_info()
        dic["Destination"] = loc_names_lis[int(dic["Destination"])-1]['Name']
        return dic

    def replace_loc_name_with_num(self,dic_edit):
        loc_info = self.dlapi.get_loc_info()
        for dic in loc_info:
            if dic_edit["Destination"].lower() == dic["Name"].lower():
                dic_edit["Destination"] = dic["id"]
                return dic_edit
    
    def is_valid(self,prop_dic) -> bool:
        dic = {"Destination":"unique", "Address":"both", "Size":int, "Rooms":int,"Type":str,"Property-number":"both","Extras":str}
        get_validation = True
        loc_correct = False
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
                    return False, key
            #check if Destination is within bounds
            if key.lower() == "destination" and get_validation:
                for row in self.get_destination_name():
                    if prop_dic["Destination"].lower() == row.lower():
                        loc_correct = True
                if loc_correct == False:
                    return False, key    
                        
            if get_validation == False:

                    return False, key
        return True, key

        
    
    def get_all_prop(self):
        all_prop = self.dlapi.get_property_info()
        return all_prop


    def find_prop_id(self,id,all_prop_lis):
        if id.isdigit():
            for dic in all_prop_lis:
                if int(dic["id"]) == int(id):
                    dic = dic
                    return dic 
            return None #[{"Text":"No employee with this id"}]
        return False

    def edit_info(self,edit_prop_dic):
        #edit_prop_dic = self.replace_loc_name_with_num(edit_prop_dic)
        if self.is_valid(edit_prop_dic):
            #edit_prop_dic = self.replace_loc_num_with_name(edit_prop_dic)
            all_lis_prop = self.dlapi.get_property_info()
            dic = self.find_prop_id(edit_prop_dic["id"],all_lis_prop)
            prop_loc_in_lis = self.find_id_location_prop(dic,all_lis_prop)
            all_lis_prop[prop_loc_in_lis]= edit_prop_dic
            self.dlapi.change_property_info(all_lis_prop)
            return True
        return False
    
    def find_id_location_prop(self,dic,all_lis_prop):
        for i in range(len(all_lis_prop)):
            if dic == all_lis_prop[i]:
                return i


    def find_prop_by_str(self,user_string,prop_lis,key):
        ret_lis=[]
        #if user_string.replace(" ",""):
        for dic in prop_lis:
            if user_string.lower() in dic[key].lower():
                ret_lis.append(dic)
        if ret_lis == []:
            return False #skoða þetta svo filter drepur ekki forritið
        return ret_lis
        #return False


if __name__ == "__main__":
    g = PropertyLL()
    #d = g.get_all_prop()
    #d = g.find_prop_id("2",g.get_all_prop())
    #print(d[0]["id"])
    #g.edit_info({"id":"31","Destination":"Kulsuk", "Address":"lol", "Size":"2", "Rooms":"3","Type":"biiiig","Property-number":"poom street 2","Extras":"Windows"})
    print(g.find_prop_by_str("windowss",g.get_all_prop(),"Extras"))
    #print(g.get_all_prop)
    #{"Name":"John"}
    #d=g.get_destination_name()
    #print(d[0].capitalize())
 
from storage_layer.DLAPI import DlAPI
from models.property import Property

class PropertyLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_property(self,prop_lis):
        if self.is_valid(prop_lis):
            loc_name = self.replace_loc_num_with_name()
            prop_lis[0] = loc_name[int(prop_lis[0])-1]['Name']
            prop = Property(self.assign_id_cont(),prop_lis[0],prop_lis[1],prop_lis[2],prop_lis[3],prop_lis[4],prop_lis[5],prop_lis[6])
            self.dlapi.add_property(prop)
            return True
        return False

    def assign_id_cont(self):
        all_prop_lis = self.dlapi.get_property_info()
        new_id = int(all_prop_lis[len(all_prop_lis)-1]["id"])+1
        return str(new_id)
    
    def get_destination_count(self):
        all_desti_lis = self.dlapi.get_loc_info()
        desti_count = int(all_desti_lis[len(all_desti_lis)-1]["id"])
        return desti_count

    def replace_loc_num_with_name(self):
        loc_names_lis = self.dlapi.get_loc_info()
        return loc_names_lis
    
    def is_valid(self,prop_lis) -> bool:
        dic = {"destination":int, "address":"both", "size":int, "rooms":int,"type":str,"property-number":"both","extras":str}
        counter = 0
        for key in dic.keys():
            if dic[key] == str and dic[key] != "both":
                if key.lower() == "extras": #replace empty string with none for extras
                    if prop_lis[counter] == "":
                        prop_lis[counter] = "None"
                get_validation = prop_lis[counter].replace(" ", "").isalpha()
            elif dic[key] == int and dic[key] != "both":
                get_validation = prop_lis[counter].replace("-","").isdigit()
            # to check if address or property number are empty    
            if dic[key] == "both":
                if prop_lis[counter] == "":
                    return False
            #check if Destination is within bounds
            if key.lower() == "destination" and get_validation:
                if  int(prop_lis[counter]) <= 0 or int(prop_lis[counter]) > self.get_destination_count():
                    return False
            if get_validation == False:

                    return False
            counter += 1
        return True

        
    def get_all_prop_lis(self):
        all_prop = self.dlapi.get_property_info()
        ret_lis = []
        for row in all_prop:
            temp_lis = []
            for keys in row:
               temp_lis.append(row[keys])
            ret_lis.append(temp_lis)
        return ret_lis
       
    def find_prop_id(self,id):
        ret_lis = []
        if id.isdigit():
            all_prop_lis=self.dlapi.get_property_info()
            for dic in all_prop_lis:
                if int(dic["id"]) == int(id):
                    for key in dic:
                        ret_lis.append(dic[key])
                    return ret_lis 
            return None
        return False

    


if __name__ == "__main__":
    g = PropertyLL()
    d = g.find_prop_id('3')
    print(d)
#     ret_lis = []
#     for row in d:
#         temp_lis = []
#         for keys in row:
#             temp_lis.append(row[keys])
#         ret_lis.append(temp_lis)
#         temp_lis = []
#     print(ret_lis[0][1])
#         #row[keys]

    #print(d[0]['Destination'])
    #b = g.replace_loc_num_with_name()
    #print(b[0]['Name'])
    #print(g.get_destination_count())
    #g = PropertyLL()
    #g.add_contractor(["John nohands","Elton john","3549990000","00","Tórshavn"])
    # g.assign_id_cont()
from storage_layer.DLAPI import DlAPI
from models.location import Location


class LocationLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_location(self,loc_dic):
        #loc_dic["Destination"] = loc_dic["Destination"].capitalize()
        loc = Location(self.assign_id_loc(),loc_dic["Name"],loc_dic["Country"],loc_dic["Airport"],loc_dic["Phone"],loc_dic["Working-hours"],loc_dic["Manager"])
        self.dlapi.add_loc(loc)


    def assign_id_loc(self):
        all_loc_lis = self.dlapi.get_loc_info()
        if all_loc_lis == []:
            new_id = 1
        else:
            new_id = int(all_loc_lis[len(all_loc_lis)-1]["id"])+1
        return str(new_id)


if __name__ == "__main__":
    g = LocationLL()
    g.add_location({"Name":"Nuuk","Country":"Greenland","Airport":"Nan","Phone":"3548988054","Working-hours":"00","Manager":"lala"})
    #d = g.get_all_prop()
    #d = g.find_prop_id("2",g.get_all_prop())
    #print(d[0]["id"])
    #g.edit_info({"id":"31","Destination":"Kulsuk", "Address":"lol", "Size":"2", "Rooms":"3","Type":"biiiig","Property-number":"poom street 2","Extras":"Windows"})
    #print(g.find_prop_by_str("windowss",g.get_all_prop(),"Extras"))
    #print(g.get_all_prop)
    #{"Name":"John"}
    #d=g.get_destination_name()
    #print(d[0].capitalize())
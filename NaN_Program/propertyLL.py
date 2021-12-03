from storage_layer.DLAPI import DlAPI
from models.property import Property

class PropertyLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_property(self,prop_lis):
        prop = Property(self.assign_id_cont(),prop_lis[0],prop_lis[1],prop_lis[2],prop_lis[3],prop_lis[4],prop_lis[5],prop_lis[6])
        self.dlapi.add_property(prop)

    def assign_id_cont(self):
        all_prop_lis = self.dlapi.get_property_info()
        new_id = int(all_prop_lis[len(all_prop_lis)-1]["id"])+1
        return str(new_id)

    
        
        


#if __name__ == "__main__":
    #g = PropertyLL()
    #g.add_contractor(["John nohands","Elton john","3549990000","00","Tórshavn"])
    # g.assign_id_cont()
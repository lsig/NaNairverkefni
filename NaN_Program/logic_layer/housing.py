from storage_layer.DLAPI import DlAPI

class Housing:

    def __init__(self, authentication, information, amenities) -> None:
        self.authentication = authentication
        self.information = information
        self.amenities = amenities

    
    def authenticateProperty(self, authentication)-> str:
        ret_str = ''
        prop_list = DlAPI.get_property_info()
        for dictionary in prop_list:
            for key in dictionary:
                if key == self.authentication:
                    for key, value in dictionary.items():
                        ret_str += value
                    return ret_str
        

    def informationOnState(self, information):
        ret_str = ''
        prop_list = DlAPI.get_property_info()
        

    def amenitiesRequirements(self, amenities):
        prop_list = DlAPI.get_property_info()


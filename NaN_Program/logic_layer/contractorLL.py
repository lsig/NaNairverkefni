
from storage_layer.DLAPI import DlAPI
from models.contractor import Contractor

class ContractorLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_contractor(self,cont_dic,boss_loc):
        '''This function add a contractor to csv files but first the function goes to a another function to 
        check if the inputs from the ui layer is valid if it is not valid both functions returns false and the key 
        that was invalid and it returns true if the the input is valid and a empty string'''

        valid, key = self.is_valid(cont_dic)
        if valid:
            cont = Contractor(self.assign_id_cont(),cont_dic["Name"],cont_dic["Contact-name"],cont_dic["Profession"],cont_dic["Phone"],cont_dic["Working-hours"],boss_loc,None)
            self.dlapi.add_cont(cont)
            return True, key
        return False, key

    def assign_id_cont(self):
        all_cont_lis = self.dlapi.get_all_cont()
        if all_cont_lis == []:
            new_id = 1
        else:
            new_id = int(all_cont_lis[len(all_cont_lis)-1]["id"])+1
        return new_id

    def is_valid(self,cont_dic) -> bool: 
        ''' This function check if the given inputs are valid. It returns false and the key that 
         if the given input is invalid other wise it return true and  a empty
        '''
        dic = {"Name":str, "Contact-name":str,"Profession":str, "Phone":int, "Working-hours":int}
        for key in dic.keys():
            if dic[key] == str:
                if len(cont_dic[key]) > 30:
                    return False, key
                get_validation = cont_dic[key].replace(" ", "").isalpha()
            else:
                get_validation = cont_dic[key].replace("-","").isdigit()
            # to check if the phone number is a valid length    
            if key.lower() == "phone" and get_validation:
                if len(cont_dic[key]) < 7 or len(cont_dic[key]) > 15:
                    return False, key
            if key.lower() == "working-hours":
                if len(cont_dic[key]) == 5:
                    if cont_dic[key][0:2].isdigit() and cont_dic[key][3:5].isdigit():
                        lower = int(cont_dic[key][0:2])
                        higher = int(cont_dic[key][3:5])
                        if int(cont_dic[key][0:2]) <= 24 and cont_dic[key][2] == '-' and int(cont_dic[key][3:5]) <= 24 and lower < higher:
                            return True,key
                return False,key

            if get_validation == False:

                    return False, key
        return True, key
    
    def find_con_id(self,id,all_cont_lis):
        ''' this function finds the contractor with the given id and returns the dict of the contrator
        if the id is valid but it can not find any one it returns none and it returns false if the id is 
        invalid
        '''
        if id.isdigit():
            for dic in all_cont_lis:
                if int(dic["id"]) == int(id):
                    return dic 
            return None
        return False
    
    def find_con_by_str(self, user_string, con_lis, key):
        """ this function finds all the string in the con_lis that match the user_string given the key
        to saerch for
        """
        ret_lis=[]
        for dic in con_lis:
            if user_string.lower() in dic[key].lower():
                ret_lis.append(dic)
        if ret_lis == []:
            return False 
        return ret_lis

    def lis_all_cont(self): 
        ''' This function returns a lis of dict with the rating updated
        '''
        return self.update_rating()



    def update_rating(self):
        """ This functions updates the rating of the contractor from the report to give a 
        mean grade
        """
        all_cont_lis = self.dlapi.get_all_cont()
        all_rep_lis = self.dlapi.get_all_report()
        counter = 0
        for cont_dic in all_cont_lis:
            denominator = 0
            nominator = 0
            for rep_dic in all_rep_lis:
                if rep_dic["Contractor-id"] == cont_dic["id"]:
                    denominator += 1
                    nominator += int(rep_dic["Contractor-rating"])
            if denominator != 0:
                rating = nominator/denominator
                all_cont_lis[counter]["Rating(0-10)"] = str(int(rating))
            counter += 1
        self.dlapi.change_cont(all_cont_lis)
        return all_cont_lis


    def edit_info(self,edit_con_dic):
        ''' This function edits the info of a contrator 
        '''
        valid, key = self.is_valid(edit_con_dic)
        if valid:
            all_lis_cont= self.dlapi.get_all_cont()
            dic = self.find_con_id(edit_con_dic["id"],all_lis_cont)
            con_loc_in_lis = self.find_id_location_con(dic,all_lis_cont)
            all_lis_cont[con_loc_in_lis]= edit_con_dic
            self.dlapi.change_cont(all_lis_cont)
            return True, key
        return False, key
        



    def find_id_location_con(self,dic,all_lis_cont):
        ''' this function find the location of the given dict in all_lis_cont 
        '''
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
    #bool_2=g.edit_info( {"id":"4","Name":"John is not grate", "Contact-name":"Elton john","Profession":"bulider", "Phone":"35499900", "Working-hours":"00","Location":"Tórshavn","Rating(0-10)":None})
    # print(g.update_rating())
    print(g.lis_all_cont())
    

    # def print_lis(lis):
    #     print(lis)
    # print("".isdigit())
    # print_lis([1,2,34])
    # lis = [1,2,3,4,5,6]
    # print(len(lis))
    # print(lis[1:len(lis)-1])
    # print("".isdigit())


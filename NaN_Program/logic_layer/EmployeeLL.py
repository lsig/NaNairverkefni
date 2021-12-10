from storage_layer.DLAPI import DlAPI
from models.employee import Employee
from storage_layer.employeeDL import EmployeeDL


class EmployeeLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empll = EmployeeDL()
        #badb


    def assign_id_emp(self):
        all_emp_lis = self.dlapi.get_all_emp()
        if all_emp_lis == []:
            new_id = 1
        else:
            new_id = int(all_emp_lis[len(all_emp_lis)-1]["id"])+1
        return str(new_id)

#Adds employee, add manager if add location is used  
    def add_employee(self,emp_dic):
        loc_add = False
        valid = False
        if ("Country" in emp_dic) == False:#will only be true if location is added
            valid, key = self.validation(emp_dic)
        else:
            loc_add = True
        if valid or loc_add == True:
            email = self.email_generate(emp_dic["Name"])
            emp_dic["Destination"] = emp_dic["Destination"].capitalize()
            emp = Employee(self.assign_id_emp(),emp_dic["Name"],emp_dic["Social Security"],emp_dic["Address"],emp_dic["Phone"],emp_dic["GSM"],email,emp_dic["Destination"],emp_dic["Manager"])
            self.dlapi.add_emp(emp)
            return True, None #spurja afhverju key?
        return False, key

#Function used for editing location
    def edit_employee(self, edit_emp_dic):
        valid, key = self.validation(edit_emp_dic)#Bounces nack to ui if row is invalid
        if valid:
            edit_emp_dic["Destination"] = edit_emp_dic["Destination"].capitalize()
            all_list_emp = self.dlapi.get_all_emp()
            dic = self.find_emp_id(edit_emp_dic["id"], all_list_emp)

            emp_loc_in_list = self.find_id_location_emp(dic, all_list_emp)
            all_list_emp[emp_loc_in_list] = edit_emp_dic
            self.dlapi.change_emp_info(all_list_emp)
            return True, None
        return False, key

#Get location names for validation. only 3 location allowed originally. kulusuk, Tórshavn and longyearbyen
    def get_destination_name(self):
        desti_names = []
        all_desti_lis = self.dlapi.get_loc_info()
        for row in all_desti_lis:    
            desti_names.append(row["Name"])
        return desti_names

#find location index in list for edit
    def find_id_location_emp(self, dic, all_list_emp):
        for i in range(len(all_list_emp)):
            if dic == all_list_emp[i]:
                return i

#returns whole dic of employee with specific id
    def find_emp_id(self, id, all_emp_lis):
        if id.isdigit():
            for dic in all_emp_lis:
                if int(dic["id"]) == int(id):
                    return dic 
            return None
        return False
#Check if login exists
    def login_info(self, email):
        all_emp_lis = self.dlapi.get_all_emp()
        email = email + "@nanair.is"
        email = email.lower()
        for key in all_emp_lis:
            if key["Email"].lower() == email:
                dic_return = key
                return dic_return

#generates email for new employee
    def email_generate(self, name):
        name = name.replace(" ",".")
        email = name + "@nanair.is"
        all_emp_lis = self.dlapi.get_all_emp()
        for key in all_emp_lis:
            if key["Email"].lower() == email:
                email = name + self.assign_id_emp() + "@nanair.is"
        return email



#Validates all inputed information
    def validation(self, emp_dic):
        loc_correct = False
        dic = {"Name":str, "Social Security":int, "Address":"both", "Phone":int,"GSM":int, "Destination":"unique"}
        # get_validation = True
        # loc_correct = False
        for key in dic.keys():
            #get_validation
            if dic[key] == str:
                if len(emp_dic[key]) > 30 :
                    return False, key
                if key.lower() == "extras": #replace empty string with none for extras
                    if emp_dic[key] == "":
                        emp_dic[key] = "None"
                get_validation = emp_dic[key].replace(" ", "").isalpha() #Name,
            elif dic[key] == int and dic[key] != "both":
                emp_dic[key] = emp_dic[key].replace("+","")
                emp_dic[key] = emp_dic[key].replace(" ","")
                get_validation = emp_dic[key].replace("-","").isdigit() #social security, Phone, GSM

            #Both cannot be empty
            if dic[key] == "both":
                if emp_dic[key] == "" or (len(emp_dic[key]) > 25): #both annot be longer than 25
                    return False, key
            #check if Destination is within bounds
            if key.lower() == "destination" and get_validation:
                for row in self.get_destination_name():
                    if emp_dic["Destination"].lower() == row.lower():
                        loc_correct = True
                if loc_correct == False:
                    return False, key
            if (key.lower() == "phone" or key.lower() == "gsm") and get_validation:
                if 7 > len(emp_dic[key]) or len(emp_dic[key]) > 15:#phone has to be in specific length range
                    return False, key
        
            if key.lower() == "social security" and get_validation:
                if 8 > len(emp_dic[key]) or len(emp_dic[key]) > 12:#social security has to be in specific length range

                    return False, key
            if get_validation == False:

                    return False, key
        return True, key

#return all emplployees
    def list_all_employees(self):
        return self.dlapi.get_all_emp()


#searches by string
    def find_emp_by_str(self, user_str, emp_lis, key):
        ret_lis = []
        for dic in emp_lis:
            if user_str.lower() in dic[key].lower():
                ret_lis.append(dic)
        if ret_lis == []:
            return False
        return ret_lis
#find name of employee by id
    def find_employee_name(self,id):
        employee_names = self.dlapi.get_all_emp()
        for dic in employee_names:
            if int(id) == int(dic["id"]):
                emp_name = dic["Name"]
        return emp_name
#get employee destiantion
    def get_emp_location(self,id):
        emp_lis = self.dlapi.get_all_emp()
        for dic in emp_lis:
            if int(id) == int(dic["id"]):
                boss_location = dic["Destination"]
                return boss_location
        none_val = "None"
        return none_val




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

#id,Name,Social Security,Address,Phone,GSM,Email,Destination,Manager    
    def add_employee(self,emp_dic):
        loc_add = False
        valid = False
        if ("Country" in emp_dic) == False:
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


    def edit_employee(self, edit_emp_dic):
        if self.validation(edit_emp_dic):
            edit_emp_dic["Destination"] = edit_emp_dic["Destination"].capitalize()
            all_list_emp = self.dlapi.get_all_emp()
            dic = self.find_emp_id(edit_emp_dic["id"], all_list_emp)

            emp_loc_in_list = self.find_id_location_emp(dic, all_list_emp)
            all_list_emp[emp_loc_in_list] = edit_emp_dic
            self.dlapi.change_emp_info(all_list_emp)
            return True
        return False


    def get_destination_name(self):
        desti_names = []
        all_desti_lis = self.dlapi.get_loc_info()
        for row in all_desti_lis:    
            desti_names.append(row["Name"])
        return desti_names


    def find_id_location_emp(self, dic, all_list_emp):
        for i in range(len(all_list_emp)):
            if dic == all_list_emp[i]:
                return i


    def find_emp_id(self, id, all_emp_lis):
        if id.isdigit():
            for dic in all_emp_lis:
                if int(dic["id"]) == int(id):
                    return dic 
            return None
        return False

    def login_info(self, email):
        all_emp_lis = self.dlapi.get_all_emp()
        email = email + "@nanair.is"
        email = email.lower()
        for key in all_emp_lis:
            if key["Email"].lower() == email:
                dic_return = key
                return dic_return


    def email_generate(self, name):
        name = name.replace(" ",".")
        email = name + "@nanair.is"
        all_emp_lis = self.dlapi.get_all_emp()
        for key in all_emp_lis:
            if key["Email"].lower() == email:
                email = name + self.assign_id_emp() + "@nanair.is"
        return email




    def validation(self, emp_dic):
        loc_correct = False
        dic = {"Name":str, "Social Security":int, "Address":"both", "Phone":int,"GSM":int, "Destination":"unique"}
        # get_validation = True
        # loc_correct = False
        for key in dic.keys():
            #get_validation
            if dic[key] == str and dic[key] != "both":
                if key.lower() == "extras": #replace empty string with none for extras
                    if emp_dic[key] == "":
                        emp_dic[key] = "None"
                get_validation = emp_dic[key].replace(" ", "").isalpha() #Name,
            elif dic[key] == int and dic[key] != "both":
                emp_dic[key] = emp_dic[key].replace("+","")
                emp_dic[key] = emp_dic[key].replace(" ","")
                get_validation = emp_dic[key].replace("-","").isdigit() #social security, Phone, GSM

            # to check if address or property number are empty    
            if dic[key] == "both":
                if emp_dic[key] == "":
                    return False, key
            #check if Destination is within bounds
            if key.lower() == "destination" and get_validation:
                for row in self.get_destination_name():
                    if emp_dic["Destination"].lower() == row.lower():
                        loc_correct = True
                if loc_correct == False:
                    return False, key
            if key.lower() == "phone" and get_validation:
                if 7 > len(emp_dic[key]) or len(emp_dic[key]) > 15:
                    return False, key
        
            if key.lower() == "social security" and get_validation:
                if 8 > len(emp_dic[key]) or len(emp_dic[key]) > 12:
                    return False, key
            if get_validation == False:

                    return False, key
        return True, key


    def list_all_employees(self):
        return self.dlapi.get_all_emp()



    def find_emp_by_str(self, user_str, emp_lis, key):
        ret_lis = []
        for dic in emp_lis:
            if user_str.lower() in dic[key].lower():
                ret_lis.append(dic)
        if ret_lis == []:
            return False
        return ret_lis

    def find_employee_name(self,id):
        employee_names = self.dlapi.get_all_emp()
        for dic in employee_names:
            if int(id) == int(dic["id"]):
                emp_name = dic["Name"]
        return emp_name

    def get_emp_location(self,id):
        emp_lis = self.dlapi.get_all_emp()
        for dic in emp_lis:
            if int(id) == int(dic["id"]):
                boss_location = dic["Destination"]
                return boss_location
        none_val = "None"
        return none_val



if __name__ == "__main__":
    e = EmployeeLL()
    #e.add_employee({"Name": "John", "Social Security": "1234567890", "Address": "Home", "Phone": "1111111", "GSM": "5555555", "Email": "John@nan.is", "Destination": "1"})
    #id,Name,Social Security,Address,Phone,GSM,Email,Destination,Manager
    #e.edit_employee({"id": "10", "Name": "Bob", "Social Security": "9876543212", "Address": "Home", "Phone": "9999999", "GSM": "5555555", "Email": "John@nan.is", "Destination": "1", "Manager": "0"})
    #print(e.email_generate("Kalli"))
    #f = {"key":"lala","lo":"sda"}
    #print("ky" in f)
    print(e.login_info("nanna.daema"))



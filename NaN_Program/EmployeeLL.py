from storage_layer.DLAPI import DlAPI
from models.employee import Employee
from storage_layer.employeeDL import EmployeeDL


class EmployeeLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empll = EmployeeDL()
        #badb


    def assign_id_job(self):
        all_emp_lis = self.dlapi.get_all_emp()
        if all_emp_lis == []:
            new_id = 1
        else:
            new_id = int(all_emp_lis[len(all_emp_lis)-1]["id"])+1
        return str(new_id)

#id,Name,Social Security,Address,Phone,GSM,Email,Destination,Manager    
    def add_employee(self,emp_dic):
        valid, key = self.validation(emp_dic)
        if valid:
            emp_dic = self.replace_loc_num_with_name(emp_dic)
            emp = Employee(self.assign_id_job(),emp_dic["Name"],emp_dic["Social Security"],emp_dic["Address"],emp_dic["Phone"],emp_dic["GSM"],emp_dic["Email"],emp_dic["Destination"],"0")
            self.dlapi.add_emp(emp)
            return True, key
        return False, key


    def edit_employee(self, edit_emp_dic):
        if self.validation(edit_emp_dic):
            edit_emp_dic = self.replace_loc_num_with_name(edit_emp_dic)
            all_list_emp = self.dlapi.get_all_emp()
            dic = self.find_emp_id(edit_emp_dic["id"], all_list_emp)

            emp_loc_in_list = self.find_id_location_emp(dic, all_list_emp)
            all_list_emp[emp_loc_in_list] = edit_emp_dic
            self.dlapi.change_emp_info(all_list_emp)
            return True
        return False




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
                dic_return = {"id": key["id"], "manager": key["Manager"]}
                return dic_return


    def validation(self, emp_dic):
        dic = {"Name":str, "Social Security":int, "Address":"both", "Phone":int,"GSM":int, "Email":"both", "Destination":int}
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
                if  int(emp_dic[key]) <= 0 or int(emp_dic[key]) > self.get_destination_count():
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


    def get_destination_count(self):
        all_desti_lis = self.dlapi.get_loc_info()
        desti_count = int(all_desti_lis[len(all_desti_lis)-1]["id"])
        return desti_count


    def list_all_employees(self):
        return self.dlapi.get_all_emp()

    def replace_loc_num_with_name(self,dic):
        loc_names_lis = self.dlapi.get_loc_info()
        dic["Destination"] = loc_names_lis[int(dic["Destination"])-1]['Name']
        return dic

if __name__ == "__main__":
    e = EmployeeLL()
    e.add_employee({"Name": "John", "Social Security": "1234567890", "Address": "Home", "Phone": "1111111", "GSM": "5555555", "Email": "John@nan.is", "Destination": "1"})
    #id,Name,Social Security,Address,Phone,GSM,Email,Destination,Manager
    #e.edit_employee({"id": "10", "Name": "Bob", "Social Security": "9876543212", "Address": "Home", "Phone": "9999999", "GSM": "5555555", "Email": "John@nan.is", "Destination": "1", "Manager": "0"})


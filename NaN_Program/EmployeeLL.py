from storage_layer.DLAPI import DlAPI
from models.employee import Employee
from storage_layer.employeeDL import EmployeeDL


class EmployeeLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empll = EmployeeDL()



    def add_employee(self):
        pass


    def assign_id_job(self):
        all_emp_lis = self.dlapi.get_all_emp()
        if all_emp_lis == []:
            new_id = 1
        else:
            new_id = int(all_emp_lis[len(all_emp_lis)-1]["id"])+1
        return str(new_id)

#id,Name,Social Security,Address,Phone,GSM,Email,Destination,Manager    
    def add_employee(self,cont_dic):
        #if self.is_valid(cont_dic):
        emp = Employee(self.assign_id_job(),cont_dic["Name"],cont_dic["Social Security"],cont_dic["Address"],cont_dic["Phone"],cont_dic["GSM"],cont_dic["Email"],cont_dic["Destination"],"0")
        self.dlapi.add_emp(emp)
        return True
        #return False

    def editemployee():
        pass


    def validation():
        pass

    def list_all_employees(self):
        ret_list = []
        emp_list = self.empll.get_all_employee()
        print(emp_list)
        # for dictionary in emp_list:
        #     temp_list = []
        #     for key in dictionary.keys():
        #         temp_list.append(key)
        #     for key, value in dictionary.items():
        #         temp_list.append(value)
        # ret_list.append(temp_list)
        # return ret_list





# from logic_layer.EmployeeLL import EmployeeLL

# class LLAPI:

#     def __init__(self):
#         self.empLL = EmployeeLL()

#     def all_employees(self):
#         return self.empLL.all_employees()

#     def create_employee(self, emp):
#         return self.empLL.create_employee(emp)

if __name__ == "__main__":
    e = EmployeeLL()
    e.add_employee({"Name": "John", "Social Security": "1234567890", "Address": "Home", "Phone": "1111111", "GSM": "5555555", "Email": "John@nan.is", "Destination": "Kulusuk"})
    #id,Name,Social Security,Address,Phone,GSM,Email,Destination,Manager    

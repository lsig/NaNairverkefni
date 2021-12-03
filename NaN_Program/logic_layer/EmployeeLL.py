from storage_layer.DLAPI import DlAPI
from models.Employee import Employee

class EmployeeLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def createemployee(self,emp_lis):
        emp = Employee(emp_lis[0], emp_list[1], emp_list[2], emp_list[3], emp_list[4], emp_list[5], emp_list[6], emp_list[7], emp_list[8])
        self.dlapi.create_emp(emp)
    

    def editemployee():
        pass

    def validation():
        pass

    def list_all_employees():
        ret_list = []
        emp_list = DlAPI.get_all_emp()
        for dictionary in emp_list:
            temp_list = []
            for key in dictionary.keys():
                temp_list.append(key)
            for key, value in dictionary.items():
                temp_list.append(value)
        ret_list.append(temp_list)
        return ret_list


if __name__ == "__main__":
    emp = EmployeeLL()
    emp.create_emp(emp)


# from logic_layer.EmployeeLL import EmployeeLL

# class LLAPI:

#     def __init__(self):
#         self.empLL = EmployeeLL()

#     def all_employees(self):
#         return self.empLL.all_employees()

#     def create_employee(self, emp):
#         return self.empLL.create_employee(emp)
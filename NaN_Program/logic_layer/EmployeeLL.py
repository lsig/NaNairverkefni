from storage_layer.DLAPI import DlAPI
from models.employee import Employee
<<<<<<< HEAD
=======
from storage_layer.employeeDL import EmployeeDL
>>>>>>> e7726cba9fb94e408f526e1fede29b3bd57d6876

class EmployeeLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empll = EmployeeDL()

    def createemployee(self,emp_lis):
        emp = Employee(emp_lis[0], emp_lis[1], emp_lis[2], emp_lis[3], emp_lis[4], emp_lis[5], emp_lis[6], emp_lis[7], emp_lis[8])
        self.dlapi.create_emp(emp)
    

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
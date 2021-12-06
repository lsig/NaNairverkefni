from storage_layer.DLAPI import DlAPI
from models.employee import Employee
from storage_layer.employeeDL import EmployeeDL


class EmployeeLL:
    def __init__(self):
        self.dlapi = DlAPI()
        self.empll = EmployeeDL()

    def createemployee(self,emp_lis):
        emp = Employee(emp_lis[0], emp_lis[1], emp_lis[2], emp_lis[3], emp_lis[4], emp_lis[5], emp_lis[6], emp_lis[7], emp_lis[8])
        self.dlapi.create_emp(emp)


    def add_employee(self):
        pass


    def assign_id_job(self):
        all_emp_lis = self.dlapi.get_all_emp()
        if all_emp_lis == []:
            new_id = 1
        else:
            new_id = int(all_emp_lis[len(all_emp_lis)-1]["id"])+1
        return str(new_id)

    
    def add_contractor(self,cont_dic):
        #if self.is_valid(cont_dic):
        cont = Employee(self.assign_id_cont(),cont_dic["Name"],cont_dic["Contact-name"],cont_dic["Profession"],cont_dic["Phone"],cont_dic["Working-hours"],cont_dic["Location"],None)
        self.dlapi.add_cont(cont)
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

if __name__ == "__main__":
    e = EmployeeLL()
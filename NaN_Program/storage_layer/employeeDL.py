import csv

class EmployeeDL:
    def __init__(self):
        self.csv = "CSV_Files/Employee.csv"

    def get_all_employee(self):
        ret_lis = []
        with open(self.csv, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_dict = {}
                for item in row:
                    temp_dict[item] = row[item]
                    # print(item,row[item])
                ret_lis.append(temp_dict)
        return ret_lis

    def add_employee(self,emp):
        with open(self.csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["id","Name","Social Security","Address","Phone ","GSM","Email","Destination","Manager"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': emp.id, "Name": emp.name, "Social Security": emp.social, "Address": emp.addr, "Phone ": emp.phone, "GSM": emp.gsm,"Email":emp.email, "Destination":emp.dest,"Manager":emp.manager})

    def change_emp_info(self,emp_lis):
        with open(self.csv, 'w+', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            header = emp_lis[0]
            writer.writerow(header)
            for dic in emp_lis:
                writer.writerow([dic["id"],dic["Name"],dic["Social Security"],dic["Address"],dic["Phone "],dic["GSM"],dic["Email"],dic["Destination"],dic["Manager"]])
        
            




if __name__ == "__main__":
    g = EmployeeDL()
    lis = g.get_all_employee()
    #emp = Employee("10","siggi","0","Traðartún 3; 108; Argir; Faroe Islands","6666666","6666667","siggi@Nanair.is","Tórshavn","0")
    g.add_employee(emp)
    g.change_emp_info(lis)
    
        
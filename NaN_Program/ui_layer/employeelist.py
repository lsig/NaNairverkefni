#starfsmannalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR
from ui_layer.boss_seeemployee import SeeEmployee
from logic_layer.LLAPI import LLAPI
from time import sleep
import os
MAXROWS = 10
EMPPRINT = [4, 20, 0, 25, 15, 15, 30, 20, 0]

class EmployeeList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.employeelist = self.llapi.get_emp_info()
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | STARFSMENN |
     - Starfsmannalisti
     {DASH*15}
     L. Leita
     B. Til baka
     /row. Breytir lengd raðar

'''
    
    def display_list(self):
        returnvalue = ''
        while returnvalue != 'B':
            self.firstrow = self.slide * self.rows 

            os.system(CLEAR)
            print(self.screen)
            for index, k in enumerate(self.employeelist[0].keys()):
                if k == 'id':
                    extra = '  '
                else:
                    extra = ''
                if k != 'Manager' and k != 'Social Security':
                    print(f"{'| ' + k + extra:<{EMPPRINT[index]}}",end='')
            print(f"\n{DASH* sum(EMPPRINT) }")

            for i in range(self.rows): #ef að við displayum self.rows starfsmenn í röð.
                try:
                    employeeinfostr = f'{self.employeelist[self.firstrow + i]["id"] + ".":<{EMPPRINT[0]}}- ' #id with some extra text.
                    for index, k in enumerate(self.employeelist[self.firstrow + i]):
                        if k == 'Address': #the address in the csv file stores town and country, seperated by semicommas (;), we only want the house address.
                            infotoprint = self.employeelist[self.firstrow + i][k].split(';')[0]
                            employeeinfostr += f"{infotoprint :<{EMPPRINT[index]}}"

                        elif k != 'id' and k != 'Manager' and k != 'Social Security': #We dont want to print the id again, and we dont want to print the manager status and social security number at all.
                            employeeinfostr += f"{self.employeelist[self.firstrow + i][k] :<{EMPPRINT[index]}}"
                    print(employeeinfostr, end='') #here we print an employee's information.
                        
                except IndexError: #if the employee id cant be found within the self.firstrow + i to self.firstrow + self.rows + i range, we get an indexerror and print an empty line.
                    pass
                print()
            
            print(f"{DASH * sum(EMPPRINT)}\n")
            if self.slide > 0:
                print("p. Previous - ", end='')
            if (self.slide + 1) * self.rows < len(self.employeelist):
                print("n. Next - ", end='')

            returnvalue = self.prompt_user()
    
    def prompt_user(self):
        user_input = input(f"#. to Select Employee\n")

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.employeelist):
            self.slide += 1

        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = int(input("Rows: ")) #validate
        
        elif user_input.upper() == 'L': #TODO
            #seeemployee = SeeEmployee(self.id) 
            pass 
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðinn starfsmann
            self.lastrow = (self.slide + 1) * self.rows + 1
            
            if self.firstrow <= int(user_input) < self.lastrow and len(self.employeelist) >= int(user_input):
                employeeinfo = self.llapi.filter_employee_id(user_input, self.employeelist) 
                seeemp = SeeEmployee(self.id, employeeinfo, self.position)
                seeemp.display()
            
            else: 
                print("Invalid row, try again!")
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)
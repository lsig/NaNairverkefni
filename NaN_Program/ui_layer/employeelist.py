#starfsmannalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from ui_layer.boss_seeemployee import SeeEmployee
from logic_layer.LLAPI import LLAPI
from time import sleep
import os
MAXROWS = 50
ROWS = 10
EMPPRINTER = [(4,'id'), (20,'SS'), (20,'Name'), (25, 'address') , (15, 'phone'), (15, 'GSM'), (25, 'email'), (20, 'destination'), (0,'other')]
EMPPRINT = [element[0] for element in EMPPRINTER]
SEARCHFILTERS = ['Name','Email','Destination', 'Social Security']


class EmployeeList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = ROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.employeelist = self.llapi.get_emp_info()
        self.employeelist_backup = self.llapi.get_emp_info()
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
    def run_screen(self):
        returnvalue = ''
        while returnvalue != 'B':
            self.display_list()
            returnvalue = self.prompt_user()
    
    def display_list(self):
            self.firstrow = self.slide * self.rows 

            os.system(CLEAR)
            print(self.screen)
            self.print_header()

            self.printedids = [self.employeelist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.employeelist) > self.firstrow + i]

            for i in range(self.rows): #ef að við displayum self.rows starfsmenn í röð.
                try:
                    employeeinfostr = f'{self.printedids[i] + ".":<{EMPPRINT[0]}}- ' #id with some extra text.
                    for index, k in enumerate(self.employeelist[self.firstrow + i]):
                        
                        if k != 'id': #the address in the csv file stores town and country, seperated by semicommas (;), we only want the house address.
                            employeeinfostr += f"{'| ' + self.employeelist[self.firstrow + i][k] :<{EMPPRINT[index]}}"
                    print(employeeinfostr, end='') #here we print an employee's information.
                        
                except IndexError: #if the employee id cant be found within the self.firstrow + i to self.firstrow + self.rows + i range, we get an indexerror and print an empty line.
                    pass
                print()
            
            self.print_footer()
    
    def prompt_user(self, oldinput = None):
        if oldinput == None:
            user_input = input()
        else:
            user_input = oldinput
            print()

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.employeelist):
            self.slide += 1

        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = self.validate(None, '/ROW')
        
        elif user_input.upper() == 'L': #TODO
            self.find_employee()
        
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

    def find_employee(self):
        for index, filter in enumerate(SEARCHFILTERS):
            print(f"{index + 1}: {filter}")
        if self.employeelist != self.employeelist_backup:
            print('R: Reset')
        userint = self.validate('userint')

        if userint == 'B':
            return 'B'
        elif userint == 'R':
            self.employeelist = self.employeelist_backup
            return
        key = SEARCHFILTERS[userint - 1]
        userstring = input(f"Search in {key.lower()}: ")

        filteredlist = self.llapi.search_employee(userstring, self.employeelist, key)

        if filteredlist == False:
            print(f"The filter {key.lower()}: {userstring} did not match any result.")
            sleep(SLEEPTIME*3)
        else:
            self.employeelist = filteredlist
        

    def print_header(self):
        for index, k in enumerate(self.employeelist[0].keys()):
            if k == 'id':
                extra = '   '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{EMPPRINT[index]}}",end='')
        print(f"\n{DASH* sum(EMPPRINT) }")
    

    def print_footer(self):
        dashlen = 21
        print(f"{DASH * sum(EMPPRINT)}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
            dashlen += 14
        if (self.slide + 1) * self.rows < len(self.employeelist):
            print("n. Next - ", end='')
            dashlen += 10
        print(f"#. to Select Employee\n{DASH*dashlen}")
        


    def validate(self, userint = None, userrows = None):
        if userint is not None:
            while True:
                userint = input(" ")
                if userint.upper() == 'B':
                    return 'B'
                elif userint.upper() == 'R':
                    return 'R'
                elif userint.isdigit() == True and (1 <= int(userint) <= len(SEARCHFILTERS)):
                    return int(userint)
                
                print(INVALID)
                sleep(SLEEPTIME)
                self.display_list()
                self.prompt_user('L')
        
        if userrows is not None:
            while True:
                userrows = input("Rows: ")
                if userrows.isdigit() == True and (1 <= int(userrows)):
                    if int(userrows) > MAXROWS:
                        print(f"Keep the row length under {MAXROWS}")
                    else:
                        return int(userrows)
                else:
                    print(INVALID)
                sleep(SLEEPTIME*2)
                self.display_list()
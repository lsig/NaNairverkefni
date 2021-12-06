#Sjá ákveðinn starfsmanna
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, CONTACTTEMPLATE
from logic_layer.LLAPI import LLAPI

from time import sleep
import os



class SeeEmployee:
    def __init__(self, id, employeedict) -> None:
        self.llapi = LLAPI()
        self.id = id
        self.employee = employeedict
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | STARFSMENN |
     - Starfsmannalisti
       - {employeedict['Name']}
     {DASH*15}
     E. Edit
     B. Til baka
'''

    def display(self):
        returnvalue = ''
        while returnvalue != 'B' or returnvalue != 'C':
            self.reset_screen()
            returnvalue = self.prompt_user()
            if returnvalue == 'C':
                return


    def printemployeeinfo(self, number = None):

        employeestring = f"{'| ' + self.employee['Address'] + ' | ':^35}\n{DASH*35}\n"

        for i in range(len(CONTACTTEMPLATE)):
            if number != None and i == number - 1:
                employeestring += f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} ____\n"
            else:
                employeestring += f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} {self.employee[CONTACTTEMPLATE[i]]}\n"
        employeestring += DASH*35
        
        print(employeestring)
    
    def prompt_user(self):
        user_input = input()

        if user_input.upper() == 'B':
            return 'C'
        
        elif user_input.upper() == 'E':
            while True:
                self.change_row()
                returnvalue = self.confirm_edit()
                if returnvalue == 'B' or returnvalue == 'C':
                    return returnvalue

        else:
            print(INVALID)
            sleep(SLEEPTIME)
    
    def change_row(self):
        user_row = int(input("Row to change: "))
        self.reset_screen(user_row)

        user_input = input(f"{CONTACTTEMPLATE[user_row - 1]}: ") #TODO validate allsstaðar
        self.employee[CONTACTTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()


    def reset_screen(self, user_row = None):
        os.system(CLEAR)
        print(self.screen)
        self.printemployeeinfo(user_row)
    
    def confirm_edit(self):
        self.reset_screen()
        is_user_happy = input("C. Confirm\nE. Edit\nB. Back\n")
            
        if is_user_happy.upper() == 'C':
            self.llapi.edit_emp(self.employee)
            print("Changes saved :)")
            sleep(SLEEPTIME)
            return 'C'

        elif is_user_happy.upper() == 'B':
            return 'B'
        
        elif is_user_happy.upper() != 'E':
            print(INVALID)
            sleep(SLEEPTIME)
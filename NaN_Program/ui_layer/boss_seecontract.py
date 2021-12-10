#velja ákveðinn starfsmann
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, CONTRACTTEMPLATE
from logic_layer.LLAPI import LLAPI


from time import sleep
import os

from ui_layer.emp_reportcreate import EmpReportCreate



class SeeContract:
    def __init__(self, id, contractinfo, position) -> None:
        self.position = position
        self.llapi = LLAPI()
        self.id = id
        self.contract = contractinfo
        editornot = ''
        if self.position == 'Manager':
            if contractinfo['Status'] == '0':
                editornot = f"\n     E. Edit"
            elif contractinfo['Status'] == '1':
                editornot = f"\n     C. what"
        elif self.position == 'Employee' and contractinfo['Status'] == '0':
            editornot = f"\n     C. Create Report"
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position} 
{STAR*14}
    | VIÐHALD |
     - Verkbeiðnalisti
       - Maintenance Request
     {DASH*15}{editornot}
     B. Til baka
'''

    def display(self):
        while True:
            self.reset_screen()
            returnvalue = self.prompt_user()
            if returnvalue == 'C':
                return

    
    def printcontractinfo(self, number = None):

        contractstring = f"{'| ' + self.contract['Title'] + ' | ':^70}\n{DASH*70}\n"

        for i in range(len(CONTRACTTEMPLATE)):
            if number != None and i == number - 1:
                contractstring += f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<35} ____\n"
            else:
                contractstring += f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<35} {self.contract[CONTRACTTEMPLATE[i]]}\n"
        contractstring += DASH*70
        
        print(contractstring)
    
    
    def prompt_user(self):
        user_input = input()

        if user_input.upper() == 'B':
            return 'C'

        elif user_input.upper() == 'E' and self.position == 'Manager' and self.contract['Status'] == '0':
            while True:
                returnvalue = self.change_row()
                if returnvalue == 'C' or returnvalue == 'B':
                    return returnvalue
        
        elif self.position == 'Employee' and self.contract['Status'] == '0' and user_input.upper() == 'C':
            reportcreate = EmpReportCreate(self.id, self.contract)
            reportcreate.display()
    

        else:
            print(INVALID)
            sleep(SLEEPTIME)
    

    def change_row(self, row = None):

        if row == None:
            user_row = None
            while user_row is None:
                self.reset_screen()
                user_input = input("Row to change: ")
                user_row = self.validate(user_input)
        else:
            user_row = row + 1
        self.reset_screen(user_row)

        user_input = input(f"{CONTRACTTEMPLATE[user_row - 1]}: ")
        old_input = self.contract[CONTRACTTEMPLATE[user_row - 1]]
        self.contract[CONTRACTTEMPLATE[user_row - 1]] = user_input 

        returnvalue = self.confirm_edit(old_input, user_row)
        if returnvalue == 'B' or returnvalue == 'C':
            return returnvalue
        elif returnvalue is not None: #here we know that the returnvalue is neither a 'B' or a 'C', therefore the self.confirm_edit(self) has denied the submission and returnes the invalid key.
            row = CONTRACTTEMPLATE.index(returnvalue)


    def confirm_edit(self, old_input, user_row):
        while True:
            self.reset_screen()
            is_user_happy = input("C. Confirm\nE. Edit\nB. Back\n")
                
            if is_user_happy.upper() == 'C':
                valid, key = self.llapi.edit_rep(self.contract)
                if valid:
                    print("Changes saved!")
                    sleep(SLEEPTIME)
                    return 'C'
                else:
                    print(f"Invalid {key}!")
                    sleep(SLEEPTIME)
                    return key

            elif is_user_happy.upper() == 'B':
                self.contract[CONTRACTTEMPLATE[user_row - 1]] = old_input
                return is_user_happy.upper()
            
            elif is_user_happy.upper() == 'E':
                return None

            else:
                print(INVALID)
                sleep(SLEEPTIME)
    

    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            if 1 <= rowint <= len(CONTRACTTEMPLATE):
                return rowint
            else:
                raise ValueError
        except ValueError:
            print(INVALID)
            sleep(SLEEPTIME)
            return None
        

    def reset_screen(self, user_row = None):
        os.system(CLEAR)
        print(self.screen)
        self.printcontractinfo(user_row)
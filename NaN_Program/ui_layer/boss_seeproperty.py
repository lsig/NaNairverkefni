#velja ákveðinn starfsmann
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, PROPERTYTEMPLATE
from logic_layer.LLAPI import LLAPI
from ui_layer.reportlist import ReportList

from time import sleep
import os



class SeeProperty:
    def __init__(self, id, propertyinfo) -> None:
        self.llapi = LLAPI()
        self.id = id
        self.property = propertyinfo
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | FASTEIGNIR |
     - Fasteignalisti
       - {self.property['Address']}
     {DASH*15}
     E. Edit
     R. Property reports
     B. Til baka
'''

    def display(self):
        while True:
            self.reset_screen()
            returnvalue = self.prompt_user()
            if returnvalue == 'C':
                return

    
    def printpropertyinfo(self, number = None):

        propertystring = f"{'| ' + self.property['Address'] + ' | ':^35}\n{DASH*35}\n"

        for i in range(len(PROPERTYTEMPLATE)):
            if number != None and i == number - 1:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} ____\n"
            else:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} {self.property[PROPERTYTEMPLATE[i]]}\n"
        propertystring += DASH*35
        
        print(propertystring)
    
    
    def prompt_user(self):
        user_input = input()

        if user_input.upper() == 'B':
            return 'C'
        
        elif user_input.upper() == 'R':
            propreport = ReportList(self.id, self.property['id'])
            propreport.display_list()

        elif user_input.upper() == 'E':
            while True:
                returnvalue = self.change_row()
                if returnvalue == 'C' or returnvalue == 'B':
                    return returnvalue

        else:
            print(INVALID)
            sleep(SLEEPTIME)
    

    def change_row(self, row = None):

        if row == None:
            validrow = ''
            while validrow is not None:
                self.reset_screen()
                user_input = input("Row to change: ")
                user_row = self.validate(user_input)
        else:
            user_row = row + 1
        self.reset_screen(user_row)

        user_input = input(f"{PROPERTYTEMPLATE[user_row - 1]}: ")
        self.property[PROPERTYTEMPLATE[user_row - 1]] = user_input 

        returnvalue = self.confirm_edit()
        if returnvalue == 'B' or returnvalue == 'C':
            return returnvalue
        elif returnvalue is not None: #here we know that the returnvalue is neither a 'B' or a 'C', therefore the self.confirm_edit(self) has denied the submission and returnes the invalid key.
            row = PROPERTYTEMPLATE.index(returnvalue)


    def confirm_edit(self):
        while True:
            self.reset_screen()
            is_user_happy = input("C. Confirm\nE. Edit\nB. Back\n")
                
            if is_user_happy.upper() == 'C':
                valid, key = self.llapi.edit_prop(self.property)
                if valid:
                    print("Changes saved!")
                    sleep(SLEEPTIME)
                    return 'C'
                else:
                    print(f"Invalid {key}!")
                    sleep(SLEEPTIME)
                    return key

            elif is_user_happy.upper() == 'B' or is_user_happy.upper() == 'B':
                return is_user_happy.upper()
            
            elif is_user_happy.upper() == 'E':
                return None

            else:
                print(INVALID)
                sleep(SLEEPTIME)
    

    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            return rowint
        except ValueError:
            print(INVALID)
            sleep(SLEEPTIME)
            return None
        

    def reset_screen(self, user_row = None):
        os.system(CLEAR)
        print(self.screen)
        self.printpropertyinfo(user_row)
    
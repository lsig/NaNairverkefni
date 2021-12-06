#velja ákveðinn starfsmann
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, PROPERTYTEMPLATE
from logic_layer.LLAPI import LLAPI

from time import sleep
import os



class SeeProperty:
    def __init__(self, id, propertyinfo) -> None:
        self.llapi = LLAPI()
        self.id = id
        self.property = propertyinfo[0]
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | FASTEIGNIR |
     - Fasteignalisti
       - {self.property['Address']}
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

    
    def printpropertyinfo(self, number = None):

        propertystring = f"{'| ' + self.property['Address'] + ' | ':^35}\n{DASH*35}\n"

        for i in range(len(PROPERTYTEMPLATE)):
            if number != None and i == number - 1:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} ____\n"
            else:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} {self.property[PROPERTYTEMPLATE[i]]}\n"
        propertystring += DASH*35
        
        print(propertystring)
    
    def change_row(self):
        user_row = int(input("Row to change: "))
        self.reset_screen(user_row)

        user_input = input(f"{PROPERTYTEMPLATE[user_row - 1]}: ")
        self.property[PROPERTYTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()
    
    def prompt_user(self):
        user_input = input()

        if user_input.upper() == 'B':
            return 
        
        elif user_input.upper() == 'E':
            while True:
                self.change_row()
                returnvalue = self.confirm_edit()
                if returnvalue == 'B' or returnvalue == 'C':
                    return returnvalue

        else:
            print(INVALID)
            sleep(SLEEPTIME)
    

    def reset_screen(self, user_row = None):
        os.system(CLEAR)
        print(self.screen)
        self.printpropertyinfo(user_row)
    
    def confirm_edit(self):
        self.reset_screen()
        is_user_happy = input("C. Confirm\nE. Edit\nB. Back\n")
            
        if is_user_happy.upper() == 'C':
            #self.llapi ble
            print("Changes saved :)")
            sleep(SLEEPTIME)
            return 'C'
            

        elif is_user_happy.upper() == 'B':
            return 'B'
        
        elif is_user_happy.upper() != 'E':
            print(INVALID)
            sleep(SLEEPTIME)
#velja ákveðinn starfsmann
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, DESTINATIONTEMPLATE
from logic_layer.LLAPI import LLAPI

from time import sleep
import os
DESTINATIONTEMPLATE = DESTINATIONTEMPLATE[0:6]


class SeeDestination:
    def __init__(self, id, destinationinfo, position) -> None:
        self.position = position
        self.llapi = LLAPI()
        self.id = id
        self.destination = destinationinfo
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position} 
{STAR*14}
    | ÁFANGASTAÐUR |
     - Áfangalisti
       - {self.destination['Name']}
     {DASH*15}
     E. Edit
     R. Destination reports
     B. Til baka
'''

    def display(self):
        while True:
            self.reset_screen()
            returnvalue = self.prompt_user()
            if returnvalue == 'C':
                return

    
    def printdestinationinfo(self, number = None):

        destinationstring = f"{'| ' + self.destination['Name'] + ' | ':^35}\n{DASH*35}\n"

        for i in range(len(DESTINATIONTEMPLATE)):
            if number != None and i == number - 1:
                destinationstring += f"{i+1}. {DESTINATIONTEMPLATE[i] + ':':<17} ____\n"
            else:
                destinationstring += f"{i+1}. {DESTINATIONTEMPLATE[i] + ':':<17} {self.destination[DESTINATIONTEMPLATE[i]]}\n"
        destinationstring += DASH*35
        
        print(destinationstring)
    
    
    def prompt_user(self):
        user_input = input()

        if user_input.upper() == 'B':
            return 'C'

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
            user_row = None
            while user_row is None:
                self.reset_screen()
                user_input = input("Row to change: ")
                user_row = self.validate(user_input)
        else:
            user_row = row + 1
        self.reset_screen(user_row)

        user_input = input(f"{DESTINATIONTEMPLATE[user_row - 1]}: ")
        old_input = self.destination[DESTINATIONTEMPLATE[user_row - 1]]
        self.destination[DESTINATIONTEMPLATE[user_row - 1]] = user_input 

        returnvalue = self.confirm_edit(old_input, user_row)
        if returnvalue == 'B' or returnvalue == 'C':
            return returnvalue
        elif returnvalue is not None: #here we know that the returnvalue is neither a 'B' or a 'C', therefore the self.confirm_edit(self) has denied the submission and returnes the invalid key.
            row = DESTINATIONTEMPLATE.index(returnvalue)


    def confirm_edit(self, old_input, user_row):
        while True:
            self.reset_screen()
            is_user_happy = input("C. Confirm\nE. Edit\nB. Back\n")
                
            if is_user_happy.upper() == 'C':
                valid, key = self.llapi.edit_loc(self.destination)
                if valid:
                    print("Changes saved!")
                    sleep(SLEEPTIME)
                    return 'C'
                else:
                    print(f"Invalid {key}!")
                    sleep(SLEEPTIME)
                    return key

            elif is_user_happy.upper() == 'B':
                self.destination[DESTINATIONTEMPLATE[user_row - 1]] = old_input
                return is_user_happy.upper()
            
            elif is_user_happy.upper() == 'E':
                return None

            else:
                print(INVALID)
                sleep(SLEEPTIME)
    

    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            if 1 <= rowint <= len(DESTINATIONTEMPLATE):
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
        self.printdestinationinfo(user_row)
    
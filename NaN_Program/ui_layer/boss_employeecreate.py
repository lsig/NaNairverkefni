#skrá nýjan starfsmann
#þarf að importa klösum eins og employee

from data_files.const import CLEAR, INVALID, QUIT, STAR, DASH, SLEEPTIME, CONTACTTEMPLATE
from logic_layer.LLAPI import LLAPI
from time import sleep
import os

class BossEmployeeCreate:
    def __init__(self, id, position) -> None:
        self.position = position
        self.llapi = LLAPI()
        self.id = id
        self.contactdict = {}
        self.screen = f'''
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | EMPLOYEES |
          - Create new employee
        {DASH*15}
        {QUIT}. Quit

    | EMPLOYEE |
{DASH * 25}'''

    def display_menu(self):
        os.system(CLEAR)
        print(self.screen)

        for i in range( len(CONTACTTEMPLATE)): 
            user_input = input(f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} ") #The user puts in info for every section of the contact
            
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return

            self.contactdict[CONTACTTEMPLATE[i]] = user_input
        print(DASH*25)
        
        self.confirmcontact()

        
    def printcontactinfo(self, number = None):
        contactstring = ''

        for i in range( len(CONTACTTEMPLATE)):

            if number != None and i == number - 1:
                contactstring += f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} ____\n"

            else:
                contactstring += f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} {self.contactdict[CONTACTTEMPLATE[i]]}\n"
        contactstring += DASH*25
        
        print(contactstring)
    

    def confirmcontact(self):

        while True:
            confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            if confirm.upper() == 'C':  # TODO
                self.contactdict["Manager"] = "0" #Not boss/mby should be in logic?
                valid, key = self.llapi.add_emp(self.contactdict)

                if valid:
                    print("Employee successfully added!")
                    sleep(SLEEPTIME)
                    return

                else:
                    print(f"Invalid {key}!")
                    sleep(SLEEPTIME)
                    self.editcontactinfo( CONTACTTEMPLATE.index(key) )
        
            elif confirm.upper() == 'E':
                self.editcontactinfo()

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
    
    def editcontactinfo(self, row = None):
        if row == None:
            user_row = None
            while user_row is None:
                self.reset_screen()
                user_input = input("Row to change: ")
                user_row = self.validate(user_input)

        else:
            user_row = row + 1
        self.reset_screen(user_row)

        user_input = input(f"{CONTACTTEMPLATE[user_row - 1]}: ")
        self.contactdict[CONTACTTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()
    
    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            if 1 <= rowint <= len(CONTACTTEMPLATE):
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
        self.printcontactinfo(user_row)



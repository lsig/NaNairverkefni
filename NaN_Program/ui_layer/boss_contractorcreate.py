#skrá nýjan verktaka
from data_files.const import CLEAR, CONTRACTORTEMPLATE, INVALID, STAR, DASH, SLEEPTIME, QUIT
from time import sleep
import os
from logic_layer.LLAPI import LLAPI

class BossContractorCreate:
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.position = position
        self.id = id
        self.contractordict = {}
        self.screen = f'''
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VERKTAKAR |
     - Skrá nýja verktaka
      {DASH*15}
    Q. Hætta við

    | VERKTAKI |
{DASH * 25}'''

    def display_contractormenu(self):
        os.system(CLEAR)
        print(self.screen)

        for i in range( len(CONTRACTORTEMPLATE)): 
            user_input = input(f"{i+1}. {CONTRACTORTEMPLATE[i] + ':':<16} ") #The user puts in info for every section of the property
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return
            #check validity
            #while self.input_is_valid(user_input) == False:
                #user_input = input(f"{i+1}: {CONTRACTORTEMPLATE[i]}")
            self.contractordict[CONTRACTORTEMPLATE[i]] = user_input
        print(DASH*25)
        
        self.confirmcontractor()

        
    def printcontractorinfo(self, number = None):
        contractorstring = ''
        for i in range( len(CONTRACTORTEMPLATE)):
            if number != None and i == number - 1:
                contractorstring += f"{i+1}. {CONTRACTORTEMPLATE[i] + ':':<16} ____\n"
            else:
                contractorstring += f"{i+1}. {CONTRACTORTEMPLATE[i] + ':':<16} {self.contractordict[CONTRACTORTEMPLATE[i]]}\n"
        contractorstring += DASH*25
        
        print(contractorstring)
    

    def confirmcontractor(self):

        while True:
            confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            if confirm.upper() == 'C':
                valid, key = self.llapi.add_cont(self.contractordict)
                if valid:
                    print("Contractor succesfully added!")
                    sleep(SLEEPTIME)
                    return
                else:
                    print(f"Wrong {key}")
                    sleep(SLEEPTIME)
                    self.editcontractorinfo( CONTRACTORTEMPLATE.index(key) )
        
            elif confirm.upper() == 'E':
                self.editcontractorinfo()

            elif confirm.upper() == 'Q':
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
    
    def editcontractorinfo(self, rowchange = None):
        if rowchange == None:
            user_row = int(input("Row to change: "))
        else:
            user_row = rowchange + 1
        self.reset_screen(user_row)

        user_input = input(f"{CONTRACTORTEMPLATE[user_row - 1]}: ")
        self.contractordict[CONTRACTORTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()
    
    def reset_screen(self, user_row = None):
        os.system(CLEAR)
        print(self.screen)
        self.printcontractorinfo(user_row)
#skrá nýjan verktaka
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME, QUIT
from time import sleep
import os
CONTRACTTEMPLATE = ['Nafn verktaka', 'Kennitala starfsmanns', 'Heimasími', 'GSM sími', 'Netfang', 'Áfangastaður']

class BossContractorCreate:
    def __init__(self, id) -> None:
        self.id = id
        self.contractorlist = []
        self.screen = f'''
 Location | Name | {self.id} 
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

        for i in range( len(CONTRACTTEMPLATE)): 
            user_input = input(f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<17} ") #The user puts in info for every section of the property
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return
            #check validity
            #while self.input_is_valid(user_input) == False:
                #user_input = input(f"{i+1}: {CONTRACTTEMPLATE[i]}")
            self.contractorlist.append(user_input)
        print(DASH*25)
        
        self.confirmcontractor()

        
    def printcontractorinfo(self, number = None):
        propertystring = ''
        for i in range( len(CONTRACTTEMPLATE)):
            if number != None and i == number - 1:
                propertystring += f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<25} ____\n"
            else:
                propertystring += f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<25} {self.contractorlist[i]}\n"
        propertystring += DASH*25
        
        print(propertystring)
    

    def confirmcontractor(self):

        confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
        while True:
            if confirm.upper() == 'C':  # TODO, tengja við LL
                #Contractor(self.contractorlist)
                return
        
            elif confirm.upper() == 'E':
                self.editcontractorinfo()
                confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            elif confirm.upper() == 'Q': # QUIT??
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
                confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
    
    def editcontractorinfo(self):
        user_row = int(input("Row to change: "))
        self.reset_screen(user_row)

        user_input = input(f"{CONTRACTTEMPLATE[user_row - 1]}: ")
        self.contractorlist[user_row - 1] = user_input

        self.reset_screen()
    
    def reset_screen(self, user_row = None):
        os.system(CLEAR)
        print(self.screen)
        self.printcontractorinfo(user_row)
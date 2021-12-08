#skrá nýja verkbeiðni
from data_files.const import CLEAR, DESTINATIONTEMPLATE, INVALID, STAR, DASH, SLEEPTIME, QUIT, CONTRACTTEMPLATE
from time import sleep
import os
from logic_layer.LLAPI import LLAPI


class ContractCreate:
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.position = position
        self.id = id
        self.contractlist = {}
        self.screen = f'''
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VIÐHALD |
     - Skrá nýja verkbeiðni
      {DASH*15}
    {QUIT}. Hætta við

    | VERKBEIÐNI |
{DASH * 25}'''

    def display(self):

        os.system(CLEAR)
        print(self.screen)

        for i in range( len(CONTRACTTEMPLATE)): 
            user_input = input(f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<17} ") #The user puts in info for every section of the property
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return
            #check validity
            #while self.input_is_valid(user_input) == False:
                #user_input = input(f"{i+1}: {CONTRACTTEMPLATE[i]}")
            self.contractlist[CONTRACTTEMPLATE[i]] = user_input
        print(DASH*25)
        
        self.confirmcontract()

        
    def printcontractinfo(self, number = None):

        contractstring = ''
        for i in range( len(CONTRACTTEMPLATE)):
            if number != None and i == number - 1:
                contractstring += f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<17} ____\n"
            else:
                contractstring += f"{i+1}. {CONTRACTTEMPLATE[i] + ':':<17} {self.contractlist[i]}\n"
        contractstring += DASH*25
        
        print(contractstring)
    

    def confirmcontract(self):

        while True:
            confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
            if confirm.upper() == 'C':  # TODO
                valid, key = self.llapi.add_job(self.contractlist,self.id)
                if valid:
                    print('Contract succesfully added!')
                    sleep(SLEEPTIME)
                    return
                else:
                    print(f'Wrong {key}')
                    sleep(SLEEPTIME)
                    self.editcontractinfo(DESTINATIONTEMPLATE.index(key))
        
            elif confirm.upper() == 'E': # TODO
                self.editcontractinfo()

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
    
    def editcontractinfo(self, row = None):
        if row == None:
            user_row = None
            while user_row is None:
                self.reset_screen()
                user_input = input('Row to change: ')
                user_row = self.validate(user_input)
        else:
            user_row = row + 1
        self.reset_screen(user_row)
        user_input = input(f"{DESTINATIONTEMPLATE[user_row - 1]}: ")
        self.contractlist[DESTINATIONTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()
    
    def reset_screen(self, user_row = None):

        os.system(CLEAR)
        print(self.screen)
        self.printcontractinfo(user_row)

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


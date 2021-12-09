#skrá nýja verkbeiðni
from data_files.const import CLEAR, CONTRACTTEMPLATE, INVALID, REGCONTRACTTEMPLATE, STAR, DASH, SLEEPTIME, QUIT
from time import sleep
import os
from logic_layer.LLAPI import LLAPI


class ContractCreate:
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.position = position
        self.id = id
        self.contractdict = {}
        self.screen = f'''
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VIÐHALD |
     - Skrá nýja verkbeiðni
      {DASH*15}
    B. Back

'''
    def run_screen(self):
        self.mainttype  = ''
        while self.mainttype != 'Back':
            returnvalue = ''
            self.mainttype, self.template = self.regular_or_single()

            while returnvalue != 'B' and self.mainttype != 'Back': 
                returnvalue = self.display()


    def display(self):

        os.system(CLEAR)
        print(self.screen)

        print(f"{'| ' + self.mainttype + ' |':^35}\n{DASH * 35}")
        for i in range( len(self.template)): 
            user_input = input(f"{i+1}. {self.template[i] + ':':<30} ") #The user puts in info for every section of the property
            if user_input.upper() == 'B': #The program exits if the user inputs q, for quitting.
                return 'B'
            self.contractdict[self.template[i]] = user_input
        print(DASH*35)
        
        self.confirmcontract()

    def regular_or_single(self):
        while True:
            os.system(CLEAR)
            print(self.screen)
            mainttype = input("1. Regluleg verkbeiðni\n2. Stök verkbeiðni\n") #1. maintenance job, 2. regular job
            if mainttype == '1':
                return 'REGLULEG VERKBEIÐNI', REGCONTRACTTEMPLATE

            elif mainttype == '2':
                return 'STÖK VERKBEIÐNI', CONTRACTTEMPLATE
            
            elif mainttype.upper() == 'B':
                return 'Back', 'Easteregg'

            print(INVALID)
            sleep(SLEEPTIME)


        
    def printcontractinfo(self, number = None):

        contractstring = f"{'| ' + self.mainttype + ' |':^35}\n{DASH * 35}\n"
        for i in range( len(self.template)):
            if number != None and i == number - 1:
                contractstring += f"{i+1}. {self.template[i] + ':':<30} ____\n"
            else:
                contractstring += f"{i+1}. {self.template[i] + ':':<30} {self.contractdict[self.template[i]]}\n"
        contractstring += DASH*35
        
        print(contractstring)
    

    def confirmcontract(self):

        while True:
            confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
            if confirm.upper() == 'C':
                valid, key = self.llapi.add_job(self.contractdict, self.id['id']) #here we tell the LLAPI to add the job, it tells us if the procedure was succesful.
                if valid:
                    print('Contract succesfully added!')
                    sleep(SLEEPTIME)
                    return
                else:
                    print(f'Wrong {key}') 
                    sleep(SLEEPTIME)
                    self.editcontractinfo( self.template.index(key) )
        
            elif confirm.upper() == 'E': # TODO
                self.editcontractinfo()

            elif confirm.upper() == 'Q':
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
        user_input = input(f"{self.template[user_row - 1]}: ")
        self.contractdict[self.template[user_row - 1]] = user_input

        self.reset_screen()
    
    def reset_screen(self, user_row = None):

        os.system(CLEAR)
        print(self.screen)
        self.printcontractinfo(user_row)

    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            if 1 <= rowint <= len(self.template):
                return rowint
            else:
                raise ValueError
        except ValueError:
            print(INVALID)
            sleep(SLEEPTIME)
            return None


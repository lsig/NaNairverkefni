#skrá nýjan starfsmann
#þarf að importa klösum eins og destination

from data_files.const import CLEAR, INVALID, QUIT, STAR, DASH, SLEEPTIME, DESTINATIONTEMPLATE
from logic_layer.LLAPI import LLAPI
from time import sleep
import os

class BossDestinationCreate:
    def __init__(self, id, position) -> None:
        self.position = position
        self.llapi = LLAPI()
        self.id = id
        self.destinationdict = {}
        self.screen = f'''
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | DESTINATIONS |
          - Create new destination
        {DASH*15}
        {QUIT}. Quit

    | DESTINATION |
{DASH * 25}'''

    def display_menu(self):
        os.system(CLEAR)
        print(self.screen)

        for i in range( len(DESTINATIONTEMPLATE)): 
            user_input = input(f"{str(i+1) + '. ' + str(DESTINATIONTEMPLATE[i]) + ': ':<21}") #The user puts in info for every section of the destination
            
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return

            self.destinationdict[DESTINATIONTEMPLATE[i]] = user_input
        print(DASH*25)
        
        self.confirmdestination()

        
    def printdestinationinfo(self, number = None):
        destinationstring = ''

        for i in range( len(DESTINATIONTEMPLATE)):

            if number != None and i == number - 1:
                destinationstring += f"{i+1}. {DESTINATIONTEMPLATE[i] + ':':<17} ____\n"

            else:
                destinationstring += f"{i+1}. {DESTINATIONTEMPLATE[i] + ':':<17} {self.destinationdict[DESTINATIONTEMPLATE[i]]}\n"
        destinationstring += DASH*25
        
        print(destinationstring)
    

    def confirmdestination(self):

        while True:
            confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            if confirm.upper() == 'C':  
                valid, key = self.llapi.add_loc(self.destinationdict)

                if valid:
                    print("Destination successfully added!")
                    sleep(SLEEPTIME)
                    return

                else:
                    print(f"Invalid {key}!")
                    sleep(SLEEPTIME)
                    self.editdestinationinfo( DESTINATIONTEMPLATE.index(key) )
        
            elif confirm.upper() == 'E':
                self.editdestinationinfo()

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
    
    def editdestinationinfo(self, row = None):
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
        self.destinationdict[DESTINATIONTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()


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



#skrá nýja fasteign
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, QUIT, PROPERTYTEMPLATE
import os 
from time import sleep
from logic_layer.LLAPI import LLAPI


class BossPropertyCreate:
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.position = position
        self.id = id
        self.propertylist = {}
        self.screen = f'''
{self.id['Destination']} | {self.id['Name']} | {self.position} 
{STAR*14}
    | FASTEIGNIR |
     - Skrá nýja fasteign
      {DASH*15}
    {QUIT}. Quit / Cancel

    | FASTEIGN |
{DASH*25}'''



    def display(self):

        os.system(CLEAR)
        print(self.screen)

        for i in range( len(PROPERTYTEMPLATE)): 
            user_input = input(f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} ") #The user puts in info for every section of the property
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return
            #check validity
            #while self.input_is_valid(user_input) == False:
                #user_input = input(f"{i+1}: {PROPERTYTEMPLATE[i]}")
            self.propertylist[PROPERTYTEMPLATE[i]] = user_input
        print(DASH*25)
        
        self.confirmproperty()

        
    def printpropertyinfo(self, number = None):

        propertystring = ''
        for i in range( len(PROPERTYTEMPLATE)):
            if number != None and i == number - 1:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} ____\n"
            else:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} {self.propertylist[PROPERTYTEMPLATE[i]]}\n"
        propertystring += DASH*25
        
        print(propertystring)
    
    #1:Kulsuk, 2:Þórshöfn, 3: longyearbyen
    def confirmproperty(self):

        while True:
            confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            if confirm.upper() == 'C':  # TODO
                valid, key = self.llapi.add_prop(self.propertylist)
                if valid: 
                    print("Property succesfully added!")
                    sleep(SLEEPTIME)
                    return
                else:
                    print(f"Wrong {key}")
                    sleep(SLEEPTIME)
                    self.editpropertyinfo( PROPERTYTEMPLATE.index(key) )
        
            elif confirm.upper() == 'E': # TODO
                self.editpropertyinfo()

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
    
    def editpropertyinfo(self, row = None):
        if row == None:
            user_row = None
            while user_row is None:
                self.reset_screen()
                user_input = input("Row to change: ")
                user_row = self.validate(user_input)
        else:
            user_row = row + 1 
        self.reset_screen(user_row)

        user_input = input(f"{PROPERTYTEMPLATE[user_row - 1]}: ")
        self.propertylist[PROPERTYTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()
    

    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            if 1 <= rowint <= len(PROPERTYTEMPLATE):
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
        self.printpropertyinfo(user_row)

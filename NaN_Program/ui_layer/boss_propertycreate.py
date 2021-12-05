#skrá nýja fasteign
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, QUIT, PROPERTYTEMPLATE
import os 
from time import sleep
from logic_layer.LLAPI import LLAPI


class BossPropertyCreate:
    def __init__(self, id) -> None:
        self.llapi = LLAPI(id)
        self.id = id
        self.propertylist = {}
        self.screen = f'''
 Location | Name | {self.id} 
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
        self.propertylist = {}
        for i in range( len(PROPERTYTEMPLATE)):
            if number != None and i == number - 1:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} ____\n"
            else:
                propertystring += f"{i+1}. {PROPERTYTEMPLATE[i] + ':':<17} {self.propertylist[i]}\n"
        propertystring += DASH*25
        
        print(propertystring)
    
    #1:Kulsuk, 2:Þórshöfn, 3: longyearbyen
    def confirmproperty(self):

        confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
        while True:
            if confirm.upper() == 'C':  # TODO
                self.llapi.add_prop(self.propertylist)
                #Property(dest_info, address_info, size_info, room_info, type_info, prop_number, extras_info)
                return
        
            elif confirm.upper() == 'E': # TODO
                self.editpropertyinfo()
                confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
                confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
    
    def editpropertyinfo(self):

        user_row = int(input("Row to change: ")) # þarf að vera tala á milli 1 og len(PROPERTYTEMPLATE) + 1
        self.reset_screen(user_row)

        user_input = input(f"{PROPERTYTEMPLATE[user_row - 1]}: ")
        self.propertylist[user_row - 1] = user_input

        self.reset_screen()
    
    def reset_screen(self, user_row = None):

        os.system(CLEAR)
        print(self.screen)
        self.printpropertyinfo(user_row)


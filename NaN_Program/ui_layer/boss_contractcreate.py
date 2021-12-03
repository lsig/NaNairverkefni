#skrá nýja verkbeiðni
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME, QUIT
from time import sleep
import os
CONTRACTTEMPLATE = ['Stofnun verkbeiðnar','Starfsmaður', 'Starfsmanna ID', 'Titill', 'Lýsing', 'Áfangastaður', 'Fasteign', 'Númer fasteignar', 'Fasteignar ID', 'Forgangur','Staða']

class ContractCreate:
    def __init__(self, id) -> None:
        self.id = id
        self.contractlist = []
        self.screen = f'''
 Location | Name | {self.id} 
{STAR*14}
    | VIÐHALD |
     - Skrá nýja verkbeiðni
      {DASH*15}
    Q. Hætta við
        '''

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
            self.contractlist.append(user_input)
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

        confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
        while True:
            if confirm.upper() == 'C':  # TODO
                #Property(dest_info, address_info, size_info, room_info, type_info, prop_number, extras_info)
                return
        
            elif confirm.upper() == 'E': # TODO
                self.editcontractinfo()
                confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
                confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
    
    def editcontractinfo(self):

        user_row = int(input("Row to change: ")) # þarf að vera tala á milli 1 og len(CONTRACTTEMPLATE) + 1
        self.reset_screen(user_row)

        user_input = input(f"{CONTRACTTEMPLATE[user_row - 1]}: ")
        self.contractlist[user_row - 1] = user_input

        self.reset_screen()
    
    def reset_screen(self, user_row = None):

        os.system(CLEAR)
        print(self.screen)
        self.printcontractinfo(user_row)




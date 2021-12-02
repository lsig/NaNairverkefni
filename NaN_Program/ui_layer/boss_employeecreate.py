#skrá nýjan starfsmann
#þarf að importa klösum eins og employee


from data_files.const import CLEAR, INVALID, QUIT, STAR, DASH, SLEEPTIME
from time import sleep
import os
CONTRACTTEMPLATE = ['Nafn', 'Kennitala', 'Heimilisfang', 'Heimasími', 'GSM símanúmer', 'Netfang', 'Áfangastaður', 'Yfirmaður']

class BossEmployeeCreate:
    def __init__(self, id) -> None:
        self.id = id
        self.contractlist = []
        self.screen = f'''
 Location | Name | {self.id} 
{STAR*14}
    | STARFSMENN |
     - Skrá nýja starfsmann
      {DASH*15}
    {QUIT}. Hætta við
        '''
    
    def display_menu(self):
        os.system(CLEAR)
        print(self.screen)

        for i in range(len(CONTRACTTEMPLATE)):
            user_input = input(f"{i+1}. {CONTRACTTEMPLATE[i]}: ")
            if user_input.upper() == QUIT:
                return
            #while check_input_validity(user_input) == False:
                #print(INVALID)
                #user_input = input(f"{i+1}. {CONTRACTTEMPLATE[i]}: ")
            self.contractlist.append(user_input)
        
        self.confirm_employee()
    
    
    def make_employee(self):
        contract_overview = f'\n{" "*17}| STARFSMAÐUR |\n'
        for i in range(len(CONTRACTTEMPLATE)):
            contract_overview += f"{CONTRACTTEMPLATE[i] + ':' :<14} {self.contractlist[i]:>35}\n"
        
        return contract_overview
    
    def confirm_employee(self):
        contract = self.make_employee()
        print(contract)
        confirm = input("""C. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
        while True:
            if confirm.upper() == 'C':  # TODO
                return
            elif confirm.upper() == 'E': # TODO
                pass
            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return
            else:
                print(INVALID)
    
 
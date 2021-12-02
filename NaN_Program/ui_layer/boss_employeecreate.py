#skrá nýjan starfsmann
#þarf að importa klösum eins og employee


from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
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
    Q. Hætta við
        '''
    
    def display_menu(self):
        os.system(CLEAR)
        print(self.screen)

        for i in range(len(CONTRACTTEMPLATE)):
            user_input = input(f"{i+1}. {CONTRACTTEMPLATE[i]}: ")
            if user_input.upper() == 'Q':
                return
            self.contractlist.append(user_input)
            #send_info(CONTRACTTEMPLATE[i], user_input)
        
        self.confirm_employee()
        
    
    def make_employee(self):
        contract_overview = '\n | STARFSMAÐUR |\n'
        listint = 0
        for i in range(len(CONTRACTTEMPLATE)):
            if self.contractlist[listint] != '':
                contract_overview += f"{CONTRACTTEMPLATE[i]}: {self.contractlist[listint]}\n"
                listint += 1
        
        return contract_overview
    
    def confirm_employee(self):
        contract = self.make_employee()
        print(contract)
        confirm = input("""C. Confirm \nE. Edit \nQ. Quit \n""")
        while True:
            if confirm.upper() == 'C':  # TODO
                return
            elif confirm.upper() == 'E': # TODO
                pass
            elif confirm.upper() == 'Q':
                return
            else:
                print(INVALID)
    
 
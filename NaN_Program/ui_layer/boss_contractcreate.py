#skrá nýja verkbeiðni
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
from time import sleep
import os
CONTRACTTEMPLATE = ['id', 'date-created', 'employee', 'employee-id', 'description', 'location', 'property', 'Property-number', 'priority', 'status']

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

        for i in range(len(CONTRACTTEMPLATE)):
            user_input = input(f"{CONTRACTTEMPLATE[i]}: ")
            if user_input.upper() == 'Q':
                return
            self.contractlist.append(user_input)
        
        self.confirm_contract()
        
    
    def make_contract(self):
        contract_overview = '\n | VERKBEIÐNI |\n'
        listint = 0
        for i in range(len(CONTRACTTEMPLATE)):
            if self.contractlist[listint] != '':
                contract_overview += f"{CONTRACTTEMPLATE[i]}: {self.contractlist[listint]}\n"
                listint += 1
        
        return contract_overview
    
    def confirm_contract(self):
        contract = self.make_contract()
        print(contract)
        confirm = input("""C. Confirm \nE. Edit \nQ. Quit \n""")
        while True:
            if confirm.upper() == 'C':  # TODO
                return
            elif confirm.upper() == 'E': # TODO
                pass
            elif confirm.upper() == 'Q': # TODO
                return
            else:
                print(INVALID)



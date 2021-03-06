#The Contractor Menu, only available for the boss.
from ui_layer.boss_contractorcreate import BossContractorCreate
from ui_layer.contractorlist import ContractorList
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
import os
from time import sleep


class BossContractorMenu:
    def __init__(self, id, position):
        self.position = position
        self.id = id
        self.options = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | CONTRACTORS |
        {DASH*15}
        1. Create new contractor
        2. Contractorlist
        {DASH*15}
        B. Back
{STAR*20}
        '''
    
    def display(self):
        '''
        displays the menu
        '''
        while True:
            os.system(CLEAR) #clears the screen
            print(self.options)
            user_choice = input()

            if user_choice == '1':
                createcontractor = BossContractorCreate(self.id, self.position)
                createcontractor.display_contractormenu()

            elif user_choice == '2':
                contractorlist = ContractorList(self.id, self.position)
                contractorlist.run_screen()

            elif user_choice.upper() == 'B':
                return
            else:
                print(INVALID) # if the user input is not one of those above it must be invalid
                sleep(SLEEPTIME)
#The maintenance menu for the boss.
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
from ui_layer.boss_contractcreate import ContractCreate
from ui_layer.whichcontractmenu import WhichContractMenu
from time import sleep
import os

from ui_layer.whichreportmenu import WhichReportMenu

class BossMaintenanceMenu:
    def __init__(self, id, position) -> None:
        self.position = position
        self.id = id
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | MAINTENANCE |
        {DASH*15}
        1. Create new contract
        2. Contractlist
        3. Reportlist
        {DASH*15}
        B. Back
{STAR*20}
        '''

    def display(self):
        '''
        Displays the menu
        '''
        while True:
            os.system(CLEAR)
            print(self.screen)
            user_input = input()

            if user_input == '1':
                contrcreate = ContractCreate(self.id, self.position)
                contrcreate.run_screen()

            elif user_input == '2':
                contrlist = WhichContractMenu(self.id, self.position)
                contrlist.init_request()

            elif user_input == '3':
                reportlist = WhichReportMenu(self.id, self.position)
                reportlist.init_request()
                

            elif user_input.upper() == 'B': 
                return #if the user inputs 'B' we return, to go back.

            else:
                print(INVALID) # if the user input is not one of those above it must be invalid
                sleep(SLEEPTIME)
#Employee Main Menu 
from ui_layer.boss_propertymenu import PropertyMenu
from ui_layer.boss_employeesmenu import BossEmployeesMenu
from ui_layer.boss_contractormenu import BossContractorMenu
from ui_layer.boss_maintenancemenu import MaintenanceMenu
import os
from time import sleep
from data_files.const import CLEAR, INVALID, QUIT, STAR, DASH, SLEEPTIME

class BossMenu: 
    def __init__(self, id):
        self.id = id
        self.options = f''' 
 Location | Name | {self.id}
{STAR*14}
      {DASH*15}
      1. Fasteignir 
      2. Starfsmenn
      3. Viðhald
      4. Verktakar
      {DASH*15}
      L. Log out
      {QUIT}. Quit 
{STAR*14}
        '''

    def print_menu(self):
        while True:   
            os.system(CLEAR) # Clears the terminal screen 
            print(self.options)
            user_choice = input()

            if user_choice == '1':
                propmenu = PropertyMenu(self.id)          # boss_propertymenu.py
                propmenu.display()

            elif user_choice == '2':
                empsmenu = BossEmployeesMenu(self.id)          # boss_employeemenu.py
                empsmenu.display()

            elif user_choice == '3':
                maintmenu = MaintenanceMenu(self.id)    # boss_maintenancemenu.py
                maintmenu.display()

            elif user_choice == '4':
                contrmenu = BossContractorMenu(self.id)      # boss_contractormenu.py
                contrmenu.display()

            elif user_choice.upper() == 'L':
                return 
            
            elif user_choice.upper() == QUIT:
                return QUIT

            else:
                print(INVALID)
                sleep(SLEEPTIME)
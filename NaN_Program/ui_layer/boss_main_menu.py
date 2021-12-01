#Employee Main Menu 
from ui_layer.boss_propertymenu import PropertyMenu
from ui_layer.boss_employeesmenu import BossEmployeesMenu
from ui_layer.boss_contractormenu import BossContractorMenu
import os
from time import sleep
STAR = '* '
DASH = '-'


class BossMenu: 
    def __init__(self,id ):
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
{STAR*14}
        '''

    def print_menu(self):
        while True:   
            os.system('clear') # Clears the terminal screen 
            print(self.options)
            user_choice = input()

            if user_choice == '1':
                propmenu = PropertyMenu(self.id)          # boss_propertymenu.py
                propmenu.display()
            elif user_choice == '2':
                empsmenu = BossEmployeesMenu(self.id)          # boss_employeemenu.py
                empsmenu.display()
            elif user_choice == '3':
                maintnence_menu = ''    # boss_maintenancemenu.py
            elif user_choice == '4':
                contract_menu = ''      # boss_contractormenu.py
            else:
                print('Invalid choice, try again!')
                sleep(1.5)
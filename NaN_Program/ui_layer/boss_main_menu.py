#Boss Main Menu 
from ui_layer.boss_destinationmenu import BossDestinationMenu
from ui_layer.boss_propertymenu import PropertyMenu
from ui_layer.boss_employeesmenu import BossEmployeesMenu
from ui_layer.boss_contractormenu import BossContractorMenu
from ui_layer.boss_maintenancemenu import BossMaintenanceMenu
import os
from time import sleep
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME

class BossMenu: 
    def __init__(self, id, position):
        self.position = position
        self.id = id
        self.options = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
        {DASH*15}
        1. Properties 
        2. Employees
        3. Maintenance
        4. Contractors
        5. Destinations
        {DASH*15}
        L. Log out
        Q. Quit 
{STAR*20}
        '''

    def print_menu(self):
        '''
        prints the menu
        '''
        while True:   
            os.system(CLEAR) # Clears the terminal screen 
            print(self.options)
            user_choice = input()

            if user_choice == '1':
                propmenu = PropertyMenu(self.id, self.position)          # boss_propertymenu.py
                propmenu.display()

            elif user_choice == '2':
                empsmenu = BossEmployeesMenu(self.id, self.position)          # boss_employeemenu.py
                empsmenu.display()

            elif user_choice == '3':
                maintmenu = BossMaintenanceMenu(self.id, self.position)    # boss_maintenancemenu.py
                maintmenu.display()

            elif user_choice == '4':
                contrmenu = BossContractorMenu(self.id, self.position)      # boss_contractormenu.py
                contrmenu.display()
            
            elif user_choice == '5':
                destmenu = BossDestinationMenu(self.id, self.position)
                destmenu.display()

            elif user_choice.upper() == 'L':
                return 
            
            elif user_choice.upper() == 'Q':
                return 'Q'

            else:
                print(INVALID) # if the user input is not one of those above it must be invalid
                sleep(SLEEPTIME)
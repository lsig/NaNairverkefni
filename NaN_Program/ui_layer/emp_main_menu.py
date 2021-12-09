#Employee Main Menu 
import os
from data_files.const import CLEAR, STAR, DASH, SLEEPTIME
from ui_layer.propertylist import PropertyList
from ui_layer.contractorlist import ContractorList
from ui_layer.emp_maintenancemenu import EmployeeMaintenanceMenu
from time import sleep

class EmployeeMenu: 
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.options = f''' 

 {self.id['Destination']} | {self.id['Name']} | {self.position} 
{STAR*18}
      {DASH*15}
      1. Fasteignir 
      2. Viðhald
      3. Verktakar
      {DASH*15}
      L. Log out
      Q. Quit 
{STAR*18}
        '''

    def print_menu(self):
        while True:   
            os.system(CLEAR)
            print(self.options)
            user_choice = input()
            
            if user_choice == '1':
                prop_menu = PropertyList(self.id, self.position)
                prop_menu.run_screen()

            elif user_choice == '2':
                maintenance_menu = EmployeeMaintenanceMenu(self.id, self.position)
                maintenance_menu.display()

            elif user_choice == '3':
                contractor_menu = ContractorList(self.id, self.position)
                contractor_menu.run_screen()
            
            elif user_choice.upper() == 'L':
                return

            elif user_choice.upper() == 'Q':
                return 'Q'

            else:
                print('Invalid choice, try again!')
                sleep(SLEEPTIME)
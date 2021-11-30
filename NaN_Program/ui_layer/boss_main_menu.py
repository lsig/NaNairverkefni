#Employee Main Menu 
from ui_layer.boss_propertymenu import PropertyMenu
from ui_layer.boss_employeesmenu import EmployeesMenu


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
        print(self.options)
        self.user_input()

    def user_input(self):
        while True:   
            user_choice = input()
            if user_choice == '1':
                propmenu = PropertyMenu()          # boss_propertymenu.py
                propmenu.open()
            elif user_choice == '2':
                empsmenu = EmployeesMenu()          # boss_employeemenu.py
                empsmenu.open()
            elif user_choice == '3':
                maintnence_menu = ''    # boss_maintenancemenu.py
            elif user_choice == '4':
                contract_menu = ''      # boss_contractormenu.py
            else:
                print('Invalid choice, try again!')
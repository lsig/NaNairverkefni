#Employee Main Menu 
import os
from data_files.const import CLEAR, STAR, DASH, SLEEPTIME
from time import sleep

class EmployeeMenu: 
    def __init__(self, id):
        self.id = id
        self.options = f''' 

 Location | Name | {self.id} 
{STAR*14}
      {DASH*15}
      1. Fasteignir 
      2. Viðhald
      3. Verktakar
      {DASH*15}
      L. Log out
      Q. Quit 
{STAR*14}
        '''

    def print_menu(self):
        while True:   
            os.system(CLEAR)
            print(self.options)
            user_choice = input()
            
            if user_choice == '1':
                prop_menu = ''

            elif user_choice == '2':
                maintnence_menu = ''

            elif user_choice == '3':
                contract_menu = ''
            
            elif user_choice.upper() == 'L':
                return

            elif user_choice.upper() == 'Q':
                return 'Q'

            else:
                print('Invalid choice, try again!')
                sleep(SLEEPTIME)
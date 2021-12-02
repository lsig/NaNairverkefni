from ui_layer.boss_employeecreate import BossEmployeeCreate
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
import os
from time import sleep
#starfsmannagluggi
#Employee Main Menu 


class BossEmployeesMenu: 
    def __init__(self, id):
        self.id = id
        self.options = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | STARFSMENN |
      {DASH*15}
      1. Skrá nýjan starfsmann
      2. Starfsmannalisti
      {DASH*15}
      B. Til baka
{STAR*14}
        '''
    
    def display(self):
        while True:
            os.system(CLEAR)
            print(self.options)
            user_choice = input()

            if user_choice == '1':
                createemployee = BossEmployeeCreate(self.id)
                createemployee.display_menu()

            elif user_choice == '2':
                emp_list = '' #TODO

            elif user_choice.upper() == 'B':
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
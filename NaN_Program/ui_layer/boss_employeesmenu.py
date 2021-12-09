from ui_layer.boss_employeecreate import BossEmployeeCreate
from ui_layer.employeelist import EmployeeList
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
import os
from time import sleep
#starfsmannagluggi
#Employee Main Menu 


class BossEmployeesMenu: 
    def __init__(self, id, position):
        self.position = position
        self.id = id
        self.options = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
         | STARFSMENN |
      {DASH*24}
      1. Skrá nýjan starfsmann
      2. Starfsmannalisti
      {DASH*24}
      B. Til baka
{STAR*20}
        '''
    
    def display(self):
        while True:
            os.system(CLEAR)
            print(self.options)
            user_choice = input()

            if user_choice == '1':
                createemployee = BossEmployeeCreate(self.id, self.position)
                createemployee.display_menu()

            elif user_choice == '2':
                emplist = EmployeeList(self.id, self.position) #This is the ui class
                emplist.run_screen()

            elif user_choice.upper() == 'B':
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
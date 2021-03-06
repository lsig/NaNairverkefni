#Employee Menu, only available for the boss. 
from ui_layer.boss_employeecreate import BossEmployeeCreate
from ui_layer.employeelist import EmployeeList
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
import os
from time import sleep



class BossEmployeesMenu: 
    def __init__(self, id, position):
        self.position = position
        self.id = id
        self.options = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | EMPLOYEES |
        {DASH*15}
        1. Create new employee
        2. Employeelist
        {DASH*15}
        B. Back
{STAR*20}
        '''
    
    def display(self):
        '''
        displays the menu
        '''
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
                print(INVALID) # if the user input is not one of those above it must be invalid
                sleep(SLEEPTIME)
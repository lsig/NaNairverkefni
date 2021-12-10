#A class for logging a user into the program, by his id.

from logic_layer.LLAPI import LLAPI
from ui_layer.boss_main_menu import BossMenu
from ui_layer.emp_main_menu import EmployeeMenu
from data_files.const import CLEAR, DASH, SLEEPTIME
import os
from time import sleep
from data_files.chucknorris import CHUCKNORRIS
import random

STAR = '*' # not the same star as in the constants 

class LoginMenu:
    def __init__(self) -> None:
        self.llapi = LLAPI() 
        self.loginscreen = f"""



 NaN Air Properties
 {STAR*18}
 {STAR + ' '*3} Enter ID {' '*3 + STAR}
 {STAR*18}
      Q. Quit
 {DASH * 18}"""

    def start(self):
        while True:
            os.system(CLEAR)
            print(random.choice(CHUCKNORRIS)) #the most important feature!
            print(self.loginscreen)
            id_input = input(' ')

            staffid = self.llapi.login_information(id_input) #we validate the user login input.

            if id_input.upper() == 'Q':    
                return

            if staffid is not None:  #if the staffid was found 
                print(f"Welcome, {staffid['Name']}")
                sleep(SLEEPTIME) 

                if staffid['Manager'] == '1': # if the user is a manager.
                    bossmenu = BossMenu(staffid, 'Manager')
                    returnvalue = bossmenu.print_menu()

                else: #else, he is an employee.
                    empmenu = EmployeeMenu(staffid, 'Employee')
                    returnvalue = empmenu.print_menu()
                
                if returnvalue == 'Q':
                        return

            else:
                print("Invalid ID, try again.")
                sleep(SLEEPTIME)

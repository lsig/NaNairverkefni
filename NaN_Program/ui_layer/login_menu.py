#Vantar að tengja Employee(): klasa við til að tengja allar upplýsingar um notanda.

from logic_layer.LLAPI import LLAPI
from ui_layer.boss_main_menu import BossMenu
from ui_layer.emp_main_menu import EmployeeMenu
from data_files.const import CLEAR, DASH, QUIT, SLEEPTIME
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
            print(self.loginscreen)
            id_input = input()

            if id_input == '': #remove for launch
                id_input = 'jan.jacobsen'

            staffid = self.llapi.login_information(id_input)

            if id_input.upper() == 'Q':    
                return

            if staffid is not None: 
                #print(f"Welcome, {staffid['Name']}")
                #sleep(SLEEPTIME*2) 
                #print(random.choice(CHUCKNORRIS))
                #sleep(SLEEPTIME*3)
                if staffid['Manager'] == '1': #TODO, vantar gagnaskrá fyrir staff id. (bossid her)
                    bossmenu = BossMenu(staffid, 'Manager')
                    returnvalue = bossmenu.print_menu()

                else:
                    empmenu = EmployeeMenu(staffid, 'Employee')
                    returnvalue = empmenu.print_menu()
                
                if returnvalue == QUIT:
                        return

            else:
                print("Invalid ID, try again.")
                sleep(SLEEPTIME+0.5)

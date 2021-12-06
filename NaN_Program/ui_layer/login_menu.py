#Vantar að tengja Employee(): klasa við til að tengja allar upplýsingar um notanda.

from logic_layer.LLAPI import LLAPI
from ui_layer.boss_main_menu import BossMenu
from ui_layer.emp_main_menu import EmployeeMenu
from data_files.const import CLEAR, DASH, QUIT, SLEEPTIME
import os
from time import sleep
STAR = '*' # not the same star as in the constants 

class LoginMenu:
    def __init__(self) -> None:
        self.llapi = LLAPI() 
        self.loginscreen = f"""
NaN Air Properties
{STAR*18}
{STAR} Enter ID:{' '*6 + STAR}
{STAR*18}

 - 's' fyrir starfsmenn, annars yfirmenn.
Q. Quit
{DASH * 14}
"""

    def start(self):
        while True:
            os.system(CLEAR)
            staffid = input(self.loginscreen)
            valid = True # = self.llapi.valid_id(staffid)
            if staffid.upper() == 'Q':    
                return

            if valid: 
                #print(f"\nWelcome, {staffid}") 
                #sleep(SLEEPTIME)
                if staffid.upper() == 'Y0301' or staffid.upper() != 'S': #TODO, vantar gagnaskrá fyrir staff id. (bossid her)
                    bossmenu = BossMenu(staffid)
                    returnvalue = bossmenu.print_menu()

                elif staffid.upper() == 'S': #TODO, (employee id hér)
                    empmenu = EmployeeMenu(staffid)
                    returnvalue = empmenu.print_menu()
                
                if returnvalue == QUIT:
                        return

            else:
                print("Invalid ID, try again.")
                sleep(SLEEPTIME-1)

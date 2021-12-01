#Vantar að tengja Employee(): klasa við til að tengja allar upplýsingar um notanda.

from logic_layer.LLAPI import LLAPI
from ui_layer.boss_main_menu import BossMenu
from ui_layer.emp_main_menu import EmployeeMenu
from data_files.const import CLEAR, SLEEPTIME
import os
from time import sleep
STAR = '*'

class LoginMenu:
    def __init__(self) -> None:
        self.llapi = LLAPI()
        self.loginscreen = f"""
NaN Air Properties
{STAR*18}
 Enter ID: """

    def start(self):
        while True:
            os.system(CLEAR)
            staffid = input(self.loginscreen)
            if staffid == 'Y0301': #TODO, vantar gagnaskrá fyrir staff id. (bossid her)
                print(f"\nWelcome, {staffid}") 
                sleep(SLEEPTIME)
                bossmenu = BossMenu(staffid)
                returnvalue = bossmenu.print_menu()
                if returnvalue == 'Q':
                    return

            elif staffid == 'S0304': #TODO, (employee id hér)
                print(f"\nWelcome, {staffid}")
                sleep(SLEEPTIME)
                empmenu = EmployeeMenu(staffid)
                empmenu.print_menu()
                
            else:
                print("Invalid ID, try again.")
                sleep(SLEEPTIME)

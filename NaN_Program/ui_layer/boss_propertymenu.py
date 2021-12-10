#The property main menu, only available for the boss.
from ui_layer.boss_propertycreate import BossPropertyCreate
from ui_layer.propertylist import PropertyList
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
import os
from time import sleep

class PropertyMenu:
    def __init__(self, id, position) -> None:
        self.id = id
        self.position = position
        self.screen =  f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | PROPERTIES |
        {DASH*15}
        1. Create new property
        2. Propertylist
        {DASH*15}
        B. Back
{STAR*20}
        '''
    
    def display(self):
        '''
        displays the menu.
        '''
        while True:
            os.system(CLEAR)
            print(self.screen)
            user_input = input()

            if user_input == '1':
                bosspropcreate = BossPropertyCreate(self.id, self.position)
                bosspropcreate.display()

            elif user_input == '2':
                proplist = PropertyList(self.id, self.position)
                proplist.run_screen()

            elif user_input.upper() == 'B':
                return
            else:
                print(INVALID) # if the user input is not one of those above it must be invalid
                sleep(SLEEPTIME)

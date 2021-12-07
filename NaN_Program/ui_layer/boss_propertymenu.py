#fasteignagluggi
from ui_layer.boss_propertycreate import BossPropertyCreate
from ui_layer.propertylist import PropertyList
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
import os
from time import sleep

class PropertyMenu:
    def __init__(self, id) -> None:
        self.id  = id
        self.screen =  f''' 
 Location | Name | {self.id}
{STAR*14}
    | FASTEIGNIR |
      {DASH*15}
      1. Skrá nýja fasteign
      2. Fasteignalisti
      {DASH*15}
      B. Til baka
{STAR*14}
        '''
    
    def display(self):
        while True:
            os.system(CLEAR)
            print(self.screen)
            user_input = input()

            if user_input == '1':
                bosspropcreate = BossPropertyCreate(self.id)
                bosspropcreate.display()

            elif user_input == '2':
                proplist = PropertyList(self.id)
                proplist.run_screen()

            elif user_input.upper() == 'B':
                return
            else:
                print(INVALID)
                sleep(SLEEPTIME)

#viðhaldsgluggi
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
from ui_layer.boss_contractcreate import ContractCreate
from time import sleep
import os

class MaintenanceMenu:
    def __init__(self, id) -> None:
        self.id = id
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | VIÐHALD |
      {DASH*15}
      1. Skrá nýja verkbeiðni
      2. Verkbeiðnalisti
      3. Verkskýrslulisti ???
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
                contrcreate = ContractCreate(self.id)
                contrcreate.display()

            elif user_input == '2':
                pass

            elif user_input == '3':
                pass

            elif user_input.upper() == 'B':
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
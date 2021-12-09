#viðhaldsgluggi
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
from ui_layer.boss_contractcreate import ContractCreate
from ui_layer.contractlist import ContractList
from ui_layer.reportlist import ReportList
from time import sleep
import os

class BossMaintenanceMenu:
    def __init__(self, id, position) -> None:
        self.position = position
        self.id = id
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VIÐHALD |
      {DASH*15}
      1. Skrá nýja verkbeiðni
      2. Verkbeiðnalisti
      3. Verkskýrslulisti
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
                contrcreate = ContractCreate(self.id, self.position)
                contrcreate.display()

            elif user_input == '2':
                contrlist = ContractList(self.id, self.position)
                contrlist.display_list()

            elif user_input == '3':
                reportlist = ReportList(self.id, self.position)
                reportlist.run_screen()
                

            elif user_input.upper() == 'B':
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
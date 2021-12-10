from ui_layer.boss_destinationcreate import BossDestinationCreate
from ui_layer.boss_destinationlist import DestinationList
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
import os
from time import sleep
#áfangastaðsgluggi
#Destination Main Menu 


class BossDestinationMenu: 
    def __init__(self, id, position):
        self.position = position
        self.id = id
        self.options = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | DESTINATIONS |
        {DASH*15}
        1. Create new destination
        2. Destinationlist
        {DASH*15}
        B. Back
{STAR*20}
        '''
    
    def display(self):
        while True:
            os.system(CLEAR)
            print(self.options)
            user_choice = input()

            if user_choice == '1':
                createdestination = BossDestinationCreate(self.id, self.position)
                createdestination.display_menu()

            elif user_choice == '2':
                emplist = DestinationList(self.id, self.position) #This is the ui class
                emplist.run_screen()

            elif user_choice.upper() == 'B':
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
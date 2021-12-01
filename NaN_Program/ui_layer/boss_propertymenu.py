#fasteignagluggi
import os
from time import sleep
STAR = '*'
DASH = '-'

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
      H. Heim
{STAR*14}
        '''
    
    def display(self):
        while True:
            os.system('clear')
            print(self.screen)
            user_input = input()

            if user_input == '1':
                pass
            elif user_input == '2':
                pass
            elif user_input.upper() == 'B':
                return
            elif user_input.upper() == 'H':
                #return 'H'
                print("Get the home option with the pro version for $9,99/month!")
            else:
                print("Invalid option! Try again.")
            
            sleep(1)

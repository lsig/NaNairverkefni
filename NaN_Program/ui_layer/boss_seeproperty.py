#velja ákveðinn starfsmann
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH

from time import sleep
import os



class SeeProperty:
    def __init__(self, id, propertyinfo) -> None:
        self.id = id
        self.property = propertyinfo[0]
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | FASTEIGNIR |
     - Fasteignalisti
       - {self.property['Address']}
     {DASH*15}
     E. Edit
     B. Til baka'''

    def display(self):
        os.system(CLEAR)
        print(self.screen)
        
        self.property_info()

        self.prompt_user()

    def property_info(self):
        print(' | '.join(self.property.values()))
    
    def prompt_user(self):
        user_input = input()

        if user_input.upper() == 'B':
            return 
        
        elif user_input.upper() == 'E':
            pass # TODO

        else:
            print(INVALID)
            sleep(SLEEPTIME)
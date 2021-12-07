#velja ákveðinn starfsmann
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH

from time import sleep
import os



class SeeContractor:
    def __init__(self, id, position) -> None:
        self.position = position
        self.id = id
        self.contractor = "Jói Spói"
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VERKTAKAR |
     - Verktakalisti
       - {self.contractor}
     {DASH*15}
     E. Edit
     B. Til baka'''

    def display(self):
        os.system(CLEAR)
        print(self.screen)
        
        self.contractor_info()

        self.prompt_user()

    def contractor_info(self):
        pass #TODO
    
    def prompt_user(self):
        user_input = input()

        if user_input.upper() == 'B':
            return 
        
        elif user_input.upper() == 'E':
            pass # TODO

        else:
            print(INVALID)
            sleep(SLEEPTIME)
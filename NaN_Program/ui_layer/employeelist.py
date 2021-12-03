#starfsmannalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from time import sleep
import os
MAXROWS = 10


class EmployeeList: 
    def __init__(self, id) -> None:
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.employeelist = [['Jói','1303576040','8776545','joi@nanair.is'], \
            ['Spói','1403579040','8876545','spoi@nanair.is'], \
            ['Gói','0903576030','','Gói@nanair.is']]
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | STARFSMENN |
     - Starfsmannalisti
     {DASH*15}
     L. Leita
     B. Til baka
     /row. Breytir lengd raðar

Nafn | Sími | Netfang | Kennitala
{DASH*35}'''
    
    def display_list(self):
        os.system(CLEAR)
        print(self.screen)
        for i in range(self.rows): #ef að við displayum 10 starfsmenn í röð.
            employeeinfostr = f'{self.slide * self.rows + i + 1}. - '
            try:
                for k in range(len(self.employeelist[self.slide * self.rows + i])):

                    employeeinfostr += f"{self.employeelist[self.slide * self.rows + i][k] :<10}"
                    
            except IndexError:
                pass
            print(employeeinfostr)
        
        
        self.prompt_user()
    
    def prompt_user(self):
        print(f"{DASH*35}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
        if (self.slide + 1) * self.rows < len(self.employeelist):
            print("n. Next - ", end='')
        
        user_input = input(f"#. to Select Employee\n")

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1
            self.display_list()

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.employeelist):
            self.slide += 1
            self.display_list()
        
        elif user_input.upper() == 'B':
            return

        elif user_input.upper() == '/ROW':
            self.rows = int(input("Rows: "))
            self.display_list()
        
        elif user_input.upper() == 'L': #TODO
            #seeemployee = SeeEmployee(self.id) 
            pass 
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðinn starfsmann
            pass

        else:
            print(INVALID)
            sleep(SLEEPTIME)
            self.display_list()





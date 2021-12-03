#verktakalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from time import sleep
import os

from ui_layer.boss_seecontractor import SeeContractor
MAXROWS = 10


class ContractorList: 
    def __init__(self, id) -> None:
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.contractorlist = [['Jói','1303576040','8776545','joi@nanair.is'],
            ['Spói','1403579040','8876545','spoi@nanair.is'],
            ['Gói','0903576030','','Gói@nanair.is'],
            ['Karl'],
            ['Siggi', '58-12345'],
            ['Maxim', 'idk'],
            ['Markús', 'newphone']]
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | VERKTAKAR |
     - Verktakalisti
     {DASH*15}
     L. Leita
     B. Til baka
     /row. Breytir lengd raðar

Nafn | Sími | Netfang | Kennitala
{DASH*35}'''
    
    def display_list(self):
        self.firstrow = self.slide * self.rows 
        os.system(CLEAR)
        print(self.screen)
        for i in range(self.rows): #til að displaya self.rows verktaka í röð.
            contractorinfostr = f'{self.firstrow + i + 1}. - '
            try:
                for k in range(len(self.contractorlist[self.firstrow + i])):
                    contractorinfostr += f"{self.contractorlist[self.firstrow + i][k] :<10}" # afh 10?
                    
            except IndexError:
                pass
            print(contractorinfostr)
        self.prompt_user()
    
    def prompt_user(self):
        print(f"{DASH*35}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
        if (self.slide + 1) * self.rows < len(self.contractorlist):
            print("n. Next - ", end='')
        
        user_input = input(f"#. to Select Contractor\n")

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1
            self.display_list()

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.contractorlist):
            self.slide += 1
            self.display_list()
        
        elif user_input.upper() == 'B':
            return

        elif user_input.upper() == '/ROW':
            self.rows = int(input("Rows: "))
            self.display_list()
        
        elif user_input.upper() == 'L': #TODO
            #seecontractor = SeeContractor(self.id) 
            pass 
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðinn verktaka
            self.lastrow = (self.slide + 1) * self.rows
            
            if self.firstrow <= int(user_input) < self.lastrow and len(self.contractorlist) >= int(user_input) :
                seecontractor = SeeContractor(self.id) 
                seecontractor.display()
            else: 
                print("Invalid row, try again!")
                sleep(SLEEPTIME)
                self.display_list()

        else:
            print(INVALID)
            sleep(SLEEPTIME)
            self.display_list()





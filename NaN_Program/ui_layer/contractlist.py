#Verkbeiðnalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10


class ContractList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.contractlist = self.llapi.get_job() 
        self.contractlist_backup = self.contractlist # er þetta ekki eih svona shallow copy, ss að ef self.contractlist breytist þá breytist self.contractlist_backup, því hann er instance.
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VIÐHALD |
     - Verkbeiðnalisti
     {DASH*15}
     L. Leita
     B. Til baka
     /row. Breytir lengd raðar

id | Destination | Address | Size | Rooms | Property number | Extras #TODO
{DASH*35}'''
    
    def display_list(self):
        returnvalue = ''
        while returnvalue != 'B':

            firstrow = self.slide * self.rows 
            os.system(CLEAR)
            print(self.screen)
            for i in range(self.rows): #til að displaya self.rows verktaka í röð.
                contractinfostr = f'{firstrow + i + 1}. - '
                try:
                    for key in self.contractlist[firstrow + i]:
                    
                        contractinfostr += f"{self.contractlist[firstrow + i][key] :<10}" # afh 10?
                        
                except IndexError:
                    pass
                print(contractinfostr)
            
            print(f"{DASH*35}\n")
            if self.slide > 0:
                print("p. Previous - ", end='')
            if (self.slide + 1) * self.rows < len(self.contractlist):
                print("n. Next - ", end='')

            returnvalue = self.prompt_user()
    
    def prompt_user(self):
        user_input = input(f"#. to Select Contract\n")

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.contractlist):
            self.slide += 1
        
        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = int(input("Rows: ")) #TODO validate 
        
        elif user_input.upper() == 'L': #TODO
            #seeproperty = SeeProperty(self.id) 
            pass 
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðna fasteign
            self.contractlist = self.contractlist_backup
            self.contractlist = self.llapi.filter_contract_id(user_input, self.contractlist)  #TODO 
            user_input = ""
            self.rows = len(self.contractlist)

        else:
            print(INVALID)
            sleep(SLEEPTIME)

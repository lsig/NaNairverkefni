#fasteignalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from ui_layer.boss_seeproperty import SeeProperty
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10


class PropertyList: 
    def __init__(self, id) -> None:
        self.llapi = LLAPI()
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.propertylist = self.llapi.get_prop_info()
        self.propertylist_backup = self.propertylist
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | FASTEIGNIR |
     - Fasteignalisti
     {DASH*15}
     L. Leita
     B. Til baka
     /row. Breytir lengd raðar

id | Destination | Address | Size | Rooms | Property number | Extras 
{DASH*35}'''
    
    def display_list(self):
        returnvalue = ''
        while returnvalue != 'B':

            #Header á ensku í bili!!!
            #self.propertylist = self.llapi.all_prop_lis()
            self.firstrow = self.slide * self.rows 
            os.system(CLEAR)
            print(self.screen)
            for i in range(self.rows): #til að displaya self.rows verktaka í röð.
                propertyinfostr = f'{self.firstrow + i + 1}. - '
                try:
                    for key in self.propertylist[self.firstrow + i]:
                    
                        propertyinfostr += f"{self.propertylist[self.firstrow + i][key] :<10}" # afh 10?
                        
                except IndexError:
                    pass
                print(propertyinfostr)
            
            print(f"{DASH*35}\n")
            if self.slide > 0:
                print("p. Previous - ", end='')
            if (self.slide + 1) * self.rows < len(self.propertylist):
                print("n. Next - ", end='')

            returnvalue = self.prompt_user()
    

    def prompt_user(self):
        user_input = input(f"#. to Select Property\n")

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.propertylist):
            self.slide += 1
        
        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = int(input("Rows: "))
        
        elif user_input.upper() == 'L': #TODO
            #seeproperty = SeeProperty(self.id) 
            pass 
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðna fasteign
            # self.propertylist = self.propertylist_backup
            # self.propertylist = self.llapi.filter_property_id(user_input, self.propertylist) 
            # user_input = ""
            # self.rows = len(self.propertylist)
            self.lastrow = (self.slide + 1) * self.rows
            
            if self.firstrow <= int(user_input) < self.lastrow and len(self.propertylist) >= int(user_input) :
                propertyinfo = self.llapi.filter_property_id(user_input, self.propertylist) 
                seeproperty = SeeProperty(self.id, propertyinfo)
                seeproperty.display()
            else: 
                print("Invalid row, try again!")
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)

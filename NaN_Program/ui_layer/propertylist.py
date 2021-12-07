#fasteignalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from ui_layer.boss_seeproperty import SeeProperty
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10
SEARCHFILTERS = ['Destination', 'Type', 'Rooms', 'Property-number']

PROPPRINT = [4, 20, 15, 8, 8, 15, 19, 10]


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

'''
    
    def display_list(self):
        returnvalue = ''
        while returnvalue != 'B':
            self.firstrow = self.slide * self.rows 
            os.system(CLEAR)
            print(self.screen)
            self.print_header()
            self.printedids = [self.propertylist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.propertylist) > self.firstrow + i]

            for i in range(self.rows): #til að displaya self.rows fasteignir í röð.
                try:
                    propertyinfost = f'{self.printedids[i] + ".":<{PROPPRINT[0]}}- ' #id with some extra text.
                    for index, k in enumerate(self.propertylist[self.firstrow + i]):

                        if k != 'id': #We dont want to print the id again.
                            propertyinfost += f"{self.propertylist[self.firstrow + i][k] :<{PROPPRINT[index]}}"
                    print(propertyinfost, end='') #here we print an employee's information.
                        
                except IndexError: #if the employee id cant be found within the self.firstrow + i to self.firstrow + self.rows + i range, we get an indexerror and print an empty line.
                    pass
                print()
            
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
        
        elif user_input.upper() == 'L':
            self.find_property()
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðna fasteign
            self.lastrow = (self.slide + 1) * self.rows + 1
            
            if user_input in self.printedids:
                propertyinfo = self.llapi.filter_property_id(user_input, self.propertylist) 
                seeproperty = SeeProperty(self.id, propertyinfo)
                seeproperty.display()
            else: 
                print(INVALID)
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)
        

    def find_property(self):
        for index, filter in enumerate(SEARCHFILTERS):
            print(f"{index + 1}: {filter}")
        userint = int(input(" "))                       #TODO Validate
        key = SEARCHFILTERS[userint - 1]
        userstring = input(f"Search {key.lower()}: ")   #TODO Validate
        
        self.propertylist = self.llapi.search_property(userstring, self.propertylist, key)
    
    def print_header(self):
        for index, k in enumerate(self.propertylist[0].keys()):
            if k == 'id':
                extra = '  '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{PROPPRINT[index]}}",end='')
        print(f"\n{DASH* sum(PROPPRINT) }")

#         id | Destination | Address | Size | Rooms | Property number | Extras 
# {DASH*35}


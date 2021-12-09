#Verkbeiðnalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10
CONTRACTPRINTER = [ (5, "id"), (12, 'Date-created'), (15, 'Employee'), (0, 'Employee-id'), (10, "Title"), (0, "Description"), (20, 'Location'), (15, 'Property'), (0, 'property-number'), (0, 'Property-id'), (15, "Priority"), (0, "Suggested-contractors(id)"), (30, "Suggested-contractors"), (0, 'Status'), (0, 'Type') ]
CONTRACTPRINT = [element[0] for element in CONTRACTPRINTER]
REGCONTRACTPRINTER = [ (5, "id"), (12, 'Date-from'), (12, 'Date-to'), (20, "Frequency"), (15, 'Employee'), (0, 'Employee-id'), (10, "Title"), (0, "Description"), (20, 'Location'), (15, 'Property'), (0, 'Propertynumber'), (0, 'propertyid'), (15, "Priority"), (30, "Suggested-contractors"), (0, "Suggested-contractors(id)"), (0, 'Status') ]
REGCONTRACTPRINT = [element[0] for element in CONTRACTPRINTER]


class ContractList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.contractlist = self.llapi.get_job()
        self.contractlist_backup = self.llapi.get_job()
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VIÐHALD |
     - Verkbeiðnalisti
     {DASH*15}
     L. Leita
     B. Til baka
     /row. Breytir lengd raðar

'''

    def run_screen(self):
        returnvalue = ''
        while returnvalue != 'B':
            self.display_list()
            returnvalue = self.prompt_user()
    
    def display_list(self):
        self.firstrow = self.slide * self.rows 

        os.system(CLEAR)
        print(self.screen)
        self.print_header()

        self.printedids = [self.contractlist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.contractlist) > self.firstrow + i]

        for i in range(self.rows): #til að displaya self.rows verktaka í röð.
            contractinfostr = f'{self.firstrow + i + 1}. - '
            try:
                for key in self.contractlist[self.firstrow + i]:
                
                    contractinfostr += f"{self.contractlist[self.firstrow + i][key] :<10}" # afh 10?
                    
            except IndexError:
                pass
            print(contractinfostr)
        
        print(f"{DASH*35}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
        if (self.slide + 1) * self.rows < len(self.contractlist):
            print("n. Next - ", end='')

    
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

            if user_input in self.printedids:
                self.contractlist = self.contractlist_backup
                self.contractlist = self.llapi.filter_contract_id(user_input, self.contractlist)  #TODO 
                user_input = ""
                self.rows = len(self.contractlist)

        else:
            print(INVALID)
            sleep(SLEEPTIME)
    

    def print_header(self):
        for index, k in enumerate(self.contractlist[0].keys()):
            if k == 'id':
                extra = '  '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{CONTRACTPRINT[index]}}",end='')
        print(f"\n{DASH* sum(CONTRACTPRINT) }")

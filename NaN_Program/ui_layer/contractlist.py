#Verkbeiðnalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR, JOBDICT
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10
CONTRACTPRINTER = [ (5, "id"), (12, 'Date-created'), (15, 'Employee'), (0, 'Employee-id'), (10, "Title"), (0, "Description"), (20, 'Location'), (15, 'Property'), (0, 'property-number'), (0, 'Property-id'), (15, "Priority"), (0, "Suggested-contractors(id)"), (30, "Suggested-contractors"), (0, 'Status'), (0, 'Type') ]
CONTRACTPRINT = [element[0] for element in CONTRACTPRINTER]
# REGCONTRACTPRINTER = [ (5, "id"), (12, 'Date-from'), (12, 'Date-to'), (20, "Frequency"), (15, 'Employee'), (0, 'Employee-id'), (10, "Title"), (0, "Description"), (20, 'Location'), (15, 'Property'), (0, 'Propertynumber'), (0, 'propertyid'), (15, "Priority"), (30, "Suggested-contractors"), (0, "Suggested-contractors(id)"), (0, 'Status') ]
# REGCONTRACTPRINT = [element[0] for element in CONTRACTPRINTER]
JOBHEADER = ['READY JOBS', 'UNREADY JOBS', 'FINISHED JOBS']


class ContractList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.contractlist = self.llapi.get_job()
        self.contractlist_backup = self.llapi.get_job()
        self.jobscount = self.llapi.count_jobs()
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

        self.rowssofar = 0

        self.printedids = []

        for index, joblist in enumerate(self.contractlist): #til að displaya self.rows verktaka í röð.
            self.rowssofar += self.print_section(JOBHEADER[index], joblist)

        
        print(f"{DASH*35}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
        if (self.slide + 1) * self.rows < self.jobscount:
            print("n. Next - ", end='')


    def print_section(self, header, section):
        print(f"\n  - {header}")
        rows = 0
        for job in section:
            if self.rowssofar + rows < self.rows:

                for key, value in job.items():
                    if key == 'id':
                        self.printedids.append(value)
                        print( f"{key + '.' :<{value}}", end='- ')

                    elif key in JOBDICT.keys():
                        print( f"{'| ' + key :<{value}}", end='')
                rows += 1
            else:
                return rows
            
        return rows




    
    def prompt_user(self):
        user_input = input(f"#. to Select Contract\n")

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < self.jobscount:
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
                self.rows = self.jobscount

        else:
            print(INVALID)
            sleep(SLEEPTIME)
    

    def print_header(self):
        for key, value in JOBDICT.items():
            if value == 'id':
                extra = '  '
            else:
                extra = ''
            print(f"{'| ' + key + extra:<{value}}",end='')
        print(f"\n{DASH* sum(JOBDICT.values()) }")

#verktakalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from ui_layer.boss_seecontractor import SeeContractor
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 50
ROWS = 10
SEARCHFILTERS = ['Name', 'Profession', 'Location', 'Rating(0-10)']

CONTRPRINT = [4, 20, 20, 12, 12, 17, 19, 15]


class ContractorList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = ROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.contractorlist = self.llapi.list_all_contractors()
        self.contractorlist_backup = self.llapi.list_all_contractors() #vantar fyrir employee
        if self.position == 'Employee':
            self.contractorlistlist = self.llapi.search_contractor(self.id['Location'], self.contractorlist,'Location' )
            self.contractorlist_backup = self.llapi.search_contractor(self.id['Location'], self.contractorlist,'Location' )
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | VERKTAKAR |
     - Verktakalisti
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

        self.printedids = [self.contractorlist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.contractorlist) > self.firstrow + i]

        for i in range(self.rows): #til að displaya self.rows verktaka í röð.
            try:
                contractorinfost = f'{self.printedids[i] + ".":<{CONTRPRINT[0]}}- ' #id with some extra text.
                for index, k in enumerate(self.contractorlist[self.firstrow + i]):

                    if k != 'id': #We dont want to print the id again.
                        contractorinfost += f"{'| ' + self.contractorlist[self.firstrow + i][k] :<{CONTRPRINT[index]}}"
                print(contractorinfost, end='') #here we print a contractor's information.
                    
            except IndexError: #if the contractor id cant be found within the self.firstrow + i to self.firstrow + self.rows + i range, we get an indexerror and print an empty line.
                pass
            print()
        
        self.print_footer()

    

    def prompt_user(self, oldinput = None):
        if oldinput == None:
            user_input = input()
        else:
            user_input = oldinput
            print()

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.contractorlist):
            self.slide += 1
        
        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = self.validate(None, '/ROW')
        
        elif user_input.upper() == 'L': #TODO
            self.find_contractor()
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðinn verktaka
            
            if user_input in self.printedids:
                contractorinfo = self.llapi.filter_contr_id(user_input, self.contractorlist)
                seecontractor = SeeContractor(self.id, contractorinfo, self.position) 
                seecontractor.display()
                self.contractorlist = self.llapi.list_all_contractors() #we want to update the list that we display, now that we may have changed info for the selected contractor.
                if self.position == 'Employee':
                    self.contractorlistlist = self.llapi.search_contractor(self.id['Location'], self.contractorlist,'Location' )
            else: 
                print(INVALID)
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)


    def find_contractor(self):
        for index, filter in enumerate(SEARCHFILTERS):
            print(f"{index + 1}: {filter}")
        if self.contractorlist != self.contractorlist_backup:
            print('R: Reset')
        userint = self.validate('userint')

        if userint == 'B':
            return 'B'
        
        elif userint == 'R' and self.contractorlist != self.contractorlist_backup:
            self.contractorlist = self.contractorlist_backup
            return

        key = SEARCHFILTERS[userint - 1]
        userstring = input(f"Search in {key.lower()}: ")

        filteredlist = self.llapi.search_contractor(userstring, self.contractorlist, key)

        if filteredlist == False:
            print(f"The filter {key.lower()}: {userstring} did not match any result.")
            sleep(SLEEPTIME*3)
        else:
            self.contractorlist = filteredlist


    def print_header(self):
        for index, k in enumerate(self.contractorlist[0].keys()):
            if k == 'id':
                extra = '  '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{CONTRPRINT[index]}}",end='')
        print(f"\n{DASH* sum(CONTRPRINT) }")
    
    
    def print_footer(self):
        dashlen = 21
        print(f"{DASH * sum(CONTRPRINT)}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
            dashlen += 14
        if (self.slide + 1) * self.rows < len(self.contractorlist):
            print("n. Next - ", end='')
            dashlen += 10
        print(f"#. to Select Contractor\n{DASH*dashlen}")
    

    def validate(self, userint = None, userrows = None):
        if userint is not None:
            while True:
                userint = input(" ")
                if userint.upper() == 'B':
                    return 'B'
                elif userint.upper() == 'R':
                    return 'R'
                elif userint.isdigit() == True and (1 <= int(userint) <= len(SEARCHFILTERS)):
                    return int(userint)
                
                print(INVALID)
                sleep(SLEEPTIME)
                self.display_list()
                self.prompt_user('L')
        
        if userrows is not None:
            while True:
                userrows = input("Rows: ")
                if userrows.isdigit() == True and (1 <= int(userrows)):
                    if int(userrows) > MAXROWS:
                        print(f"Keep the row length under {MAXROWS}")
                    else:
                        return int(userrows)
                else:
                    print(INVALID)
                sleep(SLEEPTIME*2)
                self.display_list()




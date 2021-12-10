#contractorlist window
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from ui_layer.boss_seecontractor import SeeContractor
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 50 #max row length
ROWS = 10 #default row length
SEARCHFILTERS = ['Name', 'Profession', 'Location', 'Rating(0-10)'] #controls what the user can filter the list by.

CONTRPRINT = [5, 25, 25, 20, 14, 17, 20, 15] #for indenting columns.


class ContractorList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = ROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.contractorlist = self.llapi.list_all_contractors()
        self.contractorlist_backup = self.llapi.list_all_contractors() 
        if self.position == 'Employee': #if the user is an employee we only want to see contractors in the same location as the employee.
            self.contractorlist = self.llapi.search_contractor(self.id['Destination'], self.contractorlist,'Location' )
            self.contractorlist_backup = self.llapi.search_contractor(self.id['Destination'], self.contractorlist,'Location' )
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | CONTRACTORS |
          - Contractorlist
        {DASH*15}
        L. Look
        B. Back
        /row. Change row length

'''

    def run_screen(self):
        '''
        initiates the class in a way
        '''
        returnvalue = ''
        while returnvalue != 'B':
            self.display_list()
            returnvalue = self.prompt_user()
    
    def display_list(self):
        '''
        displays the contractors in a list 
        '''
        self.firstrow = self.slide * self.rows 

        os.system(CLEAR)
        print(self.screen) #resets the screen
        self.print_header()

        self.printedids = [self.contractorlist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.contractorlist) > self.firstrow + i] #keeps info about all the id's of the contractors which were printed.

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
        '''
        promts the user for input
        '''
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
        
        elif user_input.upper() == 'L': #filter
            returnvalue = self.find_contractor()
            if returnvalue == 'B':
                return
        
        elif user_input.isdigit(): #here we select a contractor
            
            if user_input in self.printedids:
                contractorinfo = self.llapi.filter_contr_id(user_input, self.contractorlist) #here we find the contractor that we searched for.
                seecontractor = SeeContractor(self.id, contractorinfo, self.position) 
                seecontractor.display()
                self.contractorlist = self.llapi.list_all_contractors() #we want to update the list that we display, now that we may have changed info for the selected contractor.
                if self.position == 'Employee': #the same for the employee
                    self.contractorlist = self.llapi.search_contractor(self.id['Destination'], self.contractorlist,'Location' )
            else: 
                print(INVALID)
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)


    def find_contractor(self):
        '''
        takes in search parameters sends them to the 
        ll and gets back a list that is updated
        '''
        for index, filter in enumerate(SEARCHFILTERS): #here we print all different filters
            print(f"{index + 1}: {filter}")
        if self.contractorlist != self.contractorlist_backup:
            print('R: Reset')
        userint = self.validate('userint')

        if userint == 'B':
            return 'B'
        
        elif userint == 'R' and self.contractorlist != self.contractorlist_backup: #here we reset the filter
            self.contractorlist = self.contractorlist_backup
            return

        key = SEARCHFILTERS[userint - 1]
        userstring = input(f"Search in {key.lower()}: ")

        filteredlist = self.llapi.search_contractor(userstring, self.contractorlist, key) #creates the filteredlist

        if filteredlist == False: #this means that the search found no contractors.
            print(f"The filter {key.lower()}: {userstring} did not match any result.")
            sleep(SLEEPTIME*3)
        else:
            self.contractorlist = filteredlist


    def print_header(self):
        '''
        prints the header
        '''
        for index, k in enumerate(self.contractorlist[0].keys()):
            if k == 'id':
                extra = '  '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{CONTRPRINT[index]}}",end='')
        print(f"\n{DASH* sum(CONTRPRINT) }")
    
    
    def print_footer(self):
        '''
        prints the footer 
        '''
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
        '''
        validates various inputs that are easily prevantble
        '''
        if userint is not None:
            while True:
                userint = input(" ")
                if userint.upper() == 'B':
                    return 'B'
                elif userint.upper() == 'R':
                    return 'R'
                elif userint.isdigit() == True and (1 <= int(userint) <= len(SEARCHFILTERS)):
                    return int(userint) #
                
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




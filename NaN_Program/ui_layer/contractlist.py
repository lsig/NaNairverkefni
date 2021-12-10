#Verkbeiðnalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR, JOBDICT

from ui_layer.boss_seecontract import SeeContract
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10

JOBHEADER = ['READY JOBS', 'JOBS IN PROGRESS', 'FINISHED JOBS']
PRIORITYFILTER = ['emergency', 'now', 'asap']
SEARCHFILTERS = ['Priority', 'Title', 'Property', 'Employee']
CONTRACTPRINTER = [ (5, "id"), (12, 'Date-created'), (15, 'Employee'), (0, 'Employee-id'), (10, "Title"), (0, "Description"), (20, 'Location'), (15, 'Property'), (0, 'property-number'), (0, 'Property-id'), (15, "Priority"), (0, "Suggested-contractors(id)"), (30, "Suggested-contractors"), (0, 'Status'), (0, 'Type') ]
CONTRACTPRINT = [element[0] for element in CONTRACTPRINTER]

PRIORITYFILTER = ['emergency', 'now', 'asap']
SEARCHFILTERS = ['Priority(ASAP; Now; Emergency)', 'Title','Property','Employee', 'Date']


class ContractList: 
    def __init__(self, id, position, header, jobsection, info = None) -> None:
        self.llapi = LLAPI()
        self.jobsection = jobsection
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.header = header
        if jobsection == 'employee':
            allcontracts = self.llapi.get_sorted_jobs()
            self.contractlist_backup = allcontracts[1] + allcontracts[2]
            self.contractlist_backup= self.llapi.search_job(self.id['id'], self.contractlist_backup, 'Employee-id')
        else:
            self.contractlist_backup = self.llapi.get_sorted_jobs()[self.jobsection]
        self.contractlist = self.contractlist_backup

    
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | MAINTENANCE |
          - Contractlist
        {DASH*15}
        L. Look
        B. Back
        /row. Change row length

'''

    def run_screen(self):
        '''
        initates the class in a way 
        '''
        returnvalue = ''

        while returnvalue != 'B': 
            self.display_list()
            returnvalue = self.prompt_user()
    

    def display_list(self):
        '''
        displays the contract list in an orderly manner 
        '''
        self.llapi.update_reg_jobs() #this checks all regular jobs in the Regular_maintenance.csv file and checks whether any job is coming up in the near future. If so, the program adds the job to the Maintenance_request.csv

        self.firstrow = self.slide * self.rows 

        os.system(CLEAR)
        print(self.screen)
        print(f"{'| ' + self.header + ' |':^{sum(JOBDICT.values())}}" + '\n')

        self.print_header()


        self.printedids = [self.contractlist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.contractlist) > self.firstrow + i]

        if len(self.printedids) > 0:

            for i in range(self.rows): #to display self.rows contracts each time.
                try:
                    contractinfost = f'{self.printedids[i] + ".":<{JOBDICT["id"]}}- ' #id with some extra string.
                    for key in self.contractlist[self.firstrow + i]:
                        keyprint = self.contractlist[self.firstrow + i][key]

                        if key == 'Status':
                            if keyprint == '0':
                                keyprint = 'Open'
                            elif keyprint == '1':
                                keyprint = 'Ready'
                            elif keyprint == '2':
                                keyprint = 'Finished'

                        if key != 'id' and key in JOBDICT.keys(): #We dont want to print the id again.
                            contractinfost += f"{'| ' + keyprint :<{JOBDICT[key]}}"
                    print(contractinfost, end='') #here we print the contract's information.
                        
                except IndexError: #if the contract id cant be found within the self.firstrow + i to self.firstrow + self.rows + i range, we get an indexerror and print an empty line.
                    pass
                print()
        else:
            print("No results :(")
        
        self.print_footer()



    
    def prompt_user(self):
        '''
        prompts the user for input 
        '''
        user_input = input()

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.contractlist):
            self.slide += 1
        
        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = self.validate(None, '/ROW')
        
        elif user_input.upper() == 'L': #TODO
            returnvalue = self.find_job()
            if returnvalue == 'B':
                return
        
        elif user_input.isdigit(): #Here we select a contract

            if user_input in self.printedids:
                contractinfo = self.llapi.filter_job_id(user_input, self.contractlist)  #TODO 
                seecontract = SeeContract(self.id, contractinfo, self.position)
                seecontract.display()
                if self.jobsection == 'employee':
                    allcontracts = self.llapi.get_sorted_jobs()
                    self.contractlist_backup = allcontracts[1] + allcontracts[2]
                    self.contractlist_backup= self.llapi.search_job(self.id['id'], self.contractlist_backup, 'Employee-id')
                else:
                    self.contractlist_backup = self.llapi.get_sorted_jobs()[self.jobsection]
                self.contractlist = self.contractlist_backup

        else:
            print(INVALID)
            sleep(SLEEPTIME)
    

    def print_header(self):
        '''
        prints the header 
        '''
        for key, value in JOBDICT.items():
            if key == 'id':
                extra = '  '
                keyprint = key
            else:
                extra = ''
                keyprint = key
            if key == 'Priority(ASAP; Now; Emergency)':
                keyprint = 'Priority'

            print(f"{'| ' + keyprint:<{value}}",end=extra)
        print(f"\n{DASH* sum(JOBDICT.values()) }")
    

    def print_footer(self):
        '''
        prints the footer 
        '''
        print(f"{DASH* sum(JOBDICT.values())}\n")
        dashlen = 21
        if self.slide > 0:
            print("p. Previous - ", end='')
            dashlen += 14

        if (self.slide + 1) * self.rows < len(self.contractlist):
            print("n. Next - ", end='')
            dashlen += 10

        if len(self.contractlist) > 0:
            print(f"#. to Select Contract\n{DASH*dashlen}")


    def find_job(self):
        '''
        takes in search parameter, send them to the ll and gets
        back a updated list, matching the parameters
        '''
        for index, filter in enumerate(SEARCHFILTERS):
            print(f"{index + 1}: {filter}")
        if self.contractlist != self.contractlist_backup:
            print('R: Reset')
        userint = self.validate('userint')

        if userint == 'B':
            return 'B'
        elif userint == 'R' and self.contractlist != self.contractlist_backup:
            self.contractlist = self.contractlist_backup
            return
        key = SEARCHFILTERS[userint - 1]

        if key == 'Date':
            datefrom = input("Date from (dd-mm-yyyy): ")
            dateto =   input("Date to (dd-mm-yyyy): ")
            userstring = ''
            filteredlist = self.llapi.search_job_by_time(datefrom, dateto, self.contractlist)

        else:
            userstring = input(f"Search in {key.lower()}: ")
            filteredlist = self.llapi.search_job(userstring, self.contractlist, key)
            userstring = ' ' + userstring

        if filteredlist == False:
            print(f"The filter {key.lower()}:{userstring} did not match any result.")
            sleep(SLEEPTIME*3)
        else:
            self.contractlist = filteredlist
    

    def validate(self, userint = None, userrows = None):
        '''
        validates various user inputs that are easily preventable 
        '''
        if userint is not None:
            while True:
                userint = input(" ")
                if userint.upper() == 'B':
                    return 'B'
                elif userint.upper() == 'R' and self.contractlist != self.contractlist_backup:
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
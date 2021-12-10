from data_files.const import CLEAR, DASH, INVALID,SLEEPTIME, STAR, REPORTDICT
from ui_layer.boss_seereport import SeeReport
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10
REPORTHEADER = ['PENDING REPORTS', 'FINISHED REPORTS', 'OTHER REPORTS']
SEARCHFILTERS = ['Report-id', 'Employee', 'Location', 'Property', 'Date']

DONOTPRINT = ['Report-id', 'Request-id', 'Employee-id', 'Property-number', 'Property-id', 'Contractor-id']


class ReportList: 
    def __init__(self, id, position, header, jobsection, info = None, empmenu = None) -> None:
        self.empmenu = empmenu
        self.info = info
        self.llapi = LLAPI()
        self.jobsection = jobsection
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.header = header
        self.position = position
        self.menutravel = ''
        
        if jobsection == 'property':
            self.reportlist_backup = self.llapi.get_property_reports(info['id'])
        elif jobsection == 'employee':
            self.reportlist_backup = self.llapi.get_emp_reports(info['id'])
        elif jobsection == 'contractor':
            self.reportlist_backup = self.llapi.get_contractor_reports(info['id'])

        else:
            self.reportlist_backup = self.llapi.get_sorted_reports()[self.jobsection]


        self.reportlist = self.reportlist_backup
        spacebar = '        '
        if self.info == None or self.empmenu == True:
            self.menutravel = f'{spacebar}  | MAINTENANCE |\n{spacebar}  - Reportlist'
        elif jobsection == 'property':
            self.menutravel = f'{spacebar}  | PROPERTIES |\n{spacebar}  - Propertylist\n{spacebar}    - Reports: {self.info["Address"]}'
        elif jobsection == 'employee':
            self.menutravel = f'{spacebar}  | EMPLOYEES |\n{spacebar}  - Employeelist\n{spacebar}    - Reports: {self.info["Name"]}'
        elif jobsection == 'contractor':
            self.menutravel = f'{spacebar}  | CONTRACTORS |\n{spacebar}  - Contractorlist\n{spacebar}    - Reports: {self.info["Name"]}'
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position} 
{STAR*20}
{self.menutravel}
        {DASH*15}
        L. Look
        B. Back
        /row. Change row length

'''

    def run_screen(self):
        '''
        This function iniates the class
        '''
        returnvalue = ''

        while returnvalue != 'B':
            self.display_list()
            returnvalue = self.prompt_user()
    

    def display_list(self):
        '''
        This function displays the report list
        '''

        self.firstrow = self.slide * self.rows 

        os.system(CLEAR)
        print(self.screen)
        print(f"{'| ' + self.header + ' |':^{sum(REPORTDICT.values())}}" + '\n')
        
        self.print_header()

        self.printedids = [self.reportlist[self.firstrow + i]['Report-id'] for i in range(self.rows) if len(self.reportlist) > self.firstrow + i]

        if len(self.printedids) > 0:
            for i in range(self.rows): #til að displaya self.rows verktaka í röð.
                try:
                    reportinfostr = f'{self.printedids[i] + ".":<{REPORTDICT["Report-id"]}}- ' #id with some extra text.
                    for key in self.reportlist[self.firstrow + i]:
                        keyprint = self.reportlist[self.firstrow + i][key]

                        if key == 'Status':
                            if keyprint == '0':
                                keyprint = 'Declined'
                            elif keyprint == '1':
                                keyprint = 'Ready'
                            elif keyprint == '2':
                                keyprint = 'Finished'

                        if key != 'Report-id' and key in REPORTDICT.keys(): #We dont want to print the id again.
                            reportinfostr += f"{'| ' + keyprint :<{REPORTDICT[key]}}"
                    print(reportinfostr, end='') #here we print an employee's information.
                            
                except IndexError:
                    pass
                print()
        else:
            print("No results :(")

        self.print_footer()
    



    def prompt_user(self,oldinput = None):
        '''
        This function propmt the user for input
        '''
        if oldinput == None:
            user_input = input()
        else:
            user_input = oldinput
            print()

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.reportlist):
            self.slide += 1
        
        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = self.validate(None, '/ROW')
    
        elif user_input.upper() == 'L': #TODO
           returnvalue = self.find_report()
           if returnvalue == 'B':
               return
        
        elif user_input.isdigit(): #hér selectum við ákveðna fasteign

            if user_input in self.printedids:
                reportinfo = self.llapi.filter_rep_id(user_input, self.reportlist, 'Report-id')
                seereport= SeeReport(self.id, reportinfo, self.position)
                seereport.display()

            if self.jobsection == 'property':
                self.reportlist_backup = self.llapi.get_property_reports(self.info['id'])
                
            elif self.jobsection == 'employee':
                self.reportlist_backup = self.llapi.get_emp_reports(self.info['id'])

            elif self.jobsection == 'contractor':
                self.reportlist_backup = self.llapi.get_contractor_reports(self.info['id'])

            else:
                self.reportlist_backup = self.llapi.get_sorted_reports()[self.jobsection] #we want to update the list that we display, now that we may have changed info for the selected property.
            self.reportlist = self.reportlist_backup


        else:
            print(INVALID)
            sleep(SLEEPTIME)
        

    def find_report(self):
        '''
        This function takes in search parameters 
        sendt to the ll and gets an updated list back
        '''
        for index, filter in enumerate(SEARCHFILTERS):
            print(f"{index + 1}: {filter}")
        if self.reportlist != self.reportlist_backup:
            print('R: Reset')
        userint = self.validate('userint')

        if userint == 'B':
            return 'B'

        elif userint == 'R' and self.reportlist != self.reportlist_backup:
            self.reportlist = self.reportlist_backup
            return
        key = SEARCHFILTERS[userint - 1]

        if key == 'Date':
                datefrom = input("Date from (dd-mm-yyyy): ")
                dateto =   input("Date to (dd-mm-yyyy): ")
                userstring = ''
                filteredlist = self.llapi.search_job_by_time(datefrom, dateto, self.reportlist)
        
        else:
            userstring = input(f"Search in {key.lower()}: ")
            filteredlist = self.llapi.search_report(userstring, self.reportlist, key)
            userstring = ' ' + userstring

        if filteredlist == False:
            print(f"The filter {key.lower()}:{userstring} did not match any result.")
            sleep(SLEEPTIME*3)
        else:
            self.reportlist = filteredlist
        

    def print_header(self):
        '''
        default header printer
        '''
        for key, value in REPORTDICT.items():
            keyprint = key

            if key == 'Report-id':
                keyprint = 'id'
                extra = '  '
            else:
                extra = ''

            if key == 'Contractor-name':
                keyprint = 'Contractor'
            elif key == 'Contractor-rating':
                keyprint = 'Rating'
            print(f"{'| ' + keyprint:<{value}}",end=extra)

        print(f"\n{DASH * sum(REPORTDICT.values())}")
    

    def print_footer(self):
        '''
        Default printer footer
        '''
        print(f"{DASH* sum(REPORTDICT.values())}\n")
        dashlen = 21
        if self.slide > 0:
            print("p. Previous - ", end='')
            dashlen += 14

        if (self.slide + 1) * self.rows < len(self.reportlist):
            print("n. Next - ", end='')
            dashlen += 10
        
        if len(self.reportlist) > 0:
            print(f"#. to Select Report\n{DASH * dashlen}")


    def validate(self, userint = None, userrows = None):
        '''
        Validating various inputs from users which are easy to spot
        '''
        if userint is not None:
            while True:
                userint = input(" ")
                if userint.upper() == 'B':
                    return 'B'
                elif userint.upper() == 'R' and self.reportlist != self.reportlist_backup:
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
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
    def __init__(self, id, position, header, jobsection, reportdict = None) -> None:
        self.reportdict = reportdict
        self.llapi = LLAPI()
        self.jobsection = jobsection
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.header = header
        self.position = position
        self.reportlist_backup = self.llapi.get_sorted_reports()[self.jobsection]
        self.reportlist = self.reportlist_backup
        if self.reportdict == None:
            menutravel = f'    | VIÐHALD |\n     - Verkskýrslulisti'
        else:
            menutravel = f'    | FASTEIGNIR |\n     - Fasteignalisti\n       - {self.reportdict["Address"]}'
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position} 
    {STAR*14}
{menutravel}
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
        print(f"{'| ' + self.header + ' |':^{sum(REPORTDICT.values())}}" + '\n')
        
        self.print_header()

        self.printedids = [self.reportlist[self.firstrow + i]['Report-id'] for i in range(self.rows) if len(self.reportlist) > self.firstrow + i]

        if len(self.printedids) > 0:
            for i in range(self.rows): #til að displaya self.rows verktaka í röð.
                try:
                    reportinfostr = f'{self.printedids[i] + ".":<{REPORTDICT["Report-id"]}}- ' #id with some extra text.
                    for key in self.reportlist[self.firstrow + i]:

                        if key != 'Report-id' and key in REPORTDICT.keys(): #We dont want to print the id again.
                            reportinfostr += f"{'| ' + self.reportlist[self.firstrow + i][key] :<{REPORTDICT[key]}}"
                    print(reportinfostr, end='') #here we print an employee's information.
                            
                except IndexError:
                    pass
                print()
        else:
            print("No results :(")

        self.print_footer()
    



    def prompt_user(self,oldinput = None):
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
           self.find_report()
        
        elif user_input.isdigit(): #hér selectum við ákveðna fasteign

            if user_input in self.printedids:
                reportinfo = self.llapi.filter_rep_id(user_input, self.reportlist)
                seereport= SeeReport(self.id, reportinfo, self.position)
                seereport.display()
                self.reportlist = self.llapi.get_sorted_reports()[self.jobsection] #we want to update the list that we display, now that we may have changed info for the selected property.
            else: 
                print(INVALID)
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)
        

    def find_report(self):
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
        userstring = input(f"Search in {key.lower()}: ")

        filteredlist = self.llapi.search_report(userstring, self.reportlist, key)

        if filteredlist == False:
            print(f"The filter {key.lower()}: {userstring} did not match any result.")
            sleep(SLEEPTIME*3)
        else:
            self.reportlist = filteredlist
        

    def print_header(self):
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
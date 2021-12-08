from data_files.const import CLEAR, DASH, INVALID, REPORTTEMPLATE, SLEEPTIME, STAR 
from ui_layer.boss_seereport import SeeReport
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10
REPPRINT = [4,15,15,15,15]
SEARCHFILTERS = ['Title', 'Description', 'Employee', 'Contractor-rating']


class ReportList: 
    def __init__(self, id, position, reportdict = None) -> None:
        self.reportdict = reportdict
        self.llapi = LLAPI(id)
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.reportlist = self.llapi.get_report_info() #TODO
        self.reportlist_backup = self.llapi.get_report_info()
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

Report-id | Request-id | Employee | Employee-id | Title | Description |Contractor-name | Contractor-id | Contractor-rating | Status - #TODO
{DASH*35}'''

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

            self.printedids = [self.reportlist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.reportlist) > self.firstrow + i]

            for i in range(self.rows): #til að displaya self.rows verktaka í röð.
                try:
                    reportinfostr = f'{self.printedids[i] + ".":<{REPPRINT[0]}}- ' #id with some extra text.
                    for index, k in enumerate(self.reportlist[self.firstrow + i]):
                        if k != 'id': #We dont want to print the id again.
                            reportinfostr += f"{'| ' + self.reportlist[self.firstrow + i][k] :<{REPPRINT[index]}}"
                    print(reportinfostr, end='') #here we print an employee's information.
                            
                except IndexError:
                    pass
                print()

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
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðna fasteign
            self.lastrow = (self.slide + 1) * self.rows + 1
            
            if user_input in self.printedids:
                reportinfo = self.llapi.filter_rep_id(user_input, self.propertylist_backup) #as lists are mutable, we want to put the original list into filter_property_id as otherwise we would risk altering the filtered list.
                seereport= SeeReport(self.id, reportinfo, self.position)
                seereport.display()
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
        for index, k in enumerate(self.reportlist[0].keys()):
            if k == 'id':
                extra = '  '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{REPPRINT[index]}}",end='')
        print(f"\n{DASH* sum(REPPRINT) }")
    

    def print_footer(self):
        dashlen = 21
        print(f"{DASH * sum(REPPRINT)}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
            dashlen += 14
        if (self.slide + 1) * self.rows < len(self.reportlist):
            print("n. Next - ", end='')
            dashlen += 10
        print(f"#. to Select Report\n{DASH*dashlen}")


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
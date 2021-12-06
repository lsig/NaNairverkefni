from data_files.const import CLEAR, DASH, INVALID, PROPERTYTEMPLATE, SLEEPTIME, STAR 
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10


class ReportList: 
    def __init__(self, id, propertydict = None) -> None:
        self.propertydict = propertydict
        self.llapi = LLAPI(id)
        self.rows = MAXROWS
        self.slide = 0
        self.id = id
        self.reportlist = self.llapi.get_report_info() #TODO
        self.reportlist_backup = self.reportlist # er þetta ekki eih svona shallow copy, ss að ef self.reportlist breytist þá breytist self.reportlist_backup, því hann er instance.
        if self.propertydict == None:
            menutravel = f'    | VIÐHALD |\n     - Verkskýrslulisti'
        else:
            menutravel = f'    | FASTEIGNIR |\n     - Fasteignalisti\n       - {self.propertydict["Address"]}'
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
{menutravel}
     {DASH*15}
     L. Leita
     B. Til baka
     /row. Breytir lengd raðar

Report-id | Request-id | Employee | Employee-id | Title | Description |Contractor-name | Contractor-id | Contractor-rating | Status - #TODO
{DASH*35}'''
    
    def display_list(self):
        returnvalue = ''
        while returnvalue != 'B':

            firstrow = self.slide * self.rows 
            os.system(CLEAR)
            print(self.screen)
            for i in range(self.rows): #til að displaya self.rows verktaka í röð.
                reportinfostr = f'{firstrow + i + 1}. - '
                try:
                    for key in self.reportlist[firstrow + i]:
                    
                        reportinfostr += f"{self.reportlist[firstrow + i][key] :<10}" # afh 10?
                        
                except IndexError:
                    pass
                print(reportinfostr)
            
            print(f"{DASH*35}\n")
            if self.slide > 0:
                print("p. Previous - ", end='')
            if (self.slide + 1) * self.rows < len(self.reportlist):
                print("n. Next - ", end='')

            returnvalue = self.prompt_user()
    
    def prompt_user(self):
        user_input = input(f"#. to Select report\n")

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.reportlist):
            self.slide += 1
        
        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = int(input("Rows: ")) #TODO validate 
        
        elif user_input.upper() == 'L': #TODO
            #seeproperty = SeeProperty(self.id) 
            pass 
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðna fasteign
            self.reportlist = self.reportlist_backup
            self.reportlist = self.llapi.filter_report_id(user_input, self.reportlist)  #TODO 
            user_input = ""
            self.rows = len(self.reportlist)

        else:
            print(INVALID)
            sleep(SLEEPTIME)

from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR, JOBDICT

from ui_layer.contractlist import ContractList
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 10
CONTRACTPRINTER = [ (5, "id"), (12, 'Date-created'), (15, 'Employee'), (0, 'Employee-id'), (10, "Title"), (0, "Description"), (20, 'Location'), (15, 'Property'), (0, 'property-number'), (0, 'Property-id'), (15, "Priority"), (0, "Suggested-contractors(id)"), (30, "Suggested-contractors"), (0, 'Status'), (0, 'Type') ]
CONTRACTPRINT = [element[0] for element in CONTRACTPRINTER]
# REGCONTRACTPRINTER = [ (5, "id"), (12, 'Date-from'), (12, 'Date-to'), (20, "Frequency"), (15, 'Employee'), (0, 'Employee-id'), (10, "Title"), (0, "Description"), (20, 'Location'), (15, 'Property'), (0, 'Propertynumber'), (0, 'propertyid'), (15, "Priority"), (30, "Suggested-contractors"), (0, "Suggested-contractors(id)"), (0, 'Status') ]
# REGCONTRACTPRINT = [element[0] for element in CONTRACTPRINTER]
JOBHEADER = ['READY JOBS', 'JOBS IN PROGRESS', 'FINISHED JOBS']
PRIORITYFILTER = ['emergency', 'now', 'asap']
SEARCHFILTERS = ['Priority(ASAP; Now; Emergency)', 'Title','Property','Employee']

class WhichContractMenu:
    def __init__(self, id, position) -> None:
            self.llapi = LLAPI()
            self.rows = MAXROWS
            self.slide = 0
            self.id = id
            self.position = position
        
            self.screen = f''' 
    {self.id['Destination']} | {self.id['Name']} | {self.position}
    {STAR*14}
        | VIÐHALD |
        - Verkbeiðnalisti
        {DASH*15}
'''

    def which_request(self):
        while True:
            os.system(CLEAR)
            print(self.screen + self.report_choice())
            mainttype = input()
            if mainttype.isdigit() and int(mainttype) <= len(JOBHEADER):
                return int(mainttype) - 1
            elif mainttype.upper() == 'B':
                return 'B'

            print(INVALID)
            sleep(SLEEPTIME)
        

    def init_request(self):
        while True:
    
            self.reqsection = self.which_request()
            if self.reqsection == 'B':
                return

            contrlist = ContractList(self.id, self.position, JOBHEADER[int(self.reqsection)], self.reqsection)
            contrlist.run_screen()
    

    def report_choice(self):
        indentstring = '      '
        report_string = ''
        for index, word in enumerate(JOBHEADER):
            report_string += f'{indentstring}{index+1}. {word.capitalize()}\n'
        report_string += f'{indentstring}{DASH*18}\n{indentstring}B. Til baka\n{STAR*20}'
        return report_string

#A class for guiding bosses to their desired statuses of reports.
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
from ui_layer.reportlist import ReportList
REPORTHEADER = ['PENDING REPORTS', 'FINISHED REPORTS', 'OTHER REPORTS'] #different statuses of reports




class WhichReportMenu:
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.id = id
        self.position = position
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | MAINTENANCE |
          - Reportlist
        {DASH*15}
'''


    def which_request(self):
        '''
        Asks the user which report type he wants
        '''
        while True:
            os.system(CLEAR)
            print(self.screen + self.report_choice())
            mainttype = input()
            if mainttype.isdigit() and int(mainttype) <= len(REPORTHEADER):
                return int(mainttype) - 1
            elif mainttype.upper() == 'B':
                return 'B'

            print(INVALID) #if the input is neither a valid integer nor a request to go back, it is invalid
            sleep(SLEEPTIME)
        

    def init_request(self):
        '''
        runs the class, by asking for a filter and putting the filter info into the ReportList window.
        '''
        while True:
    
            self.reqsection = self.which_request()
            if self.reqsection == 'B':
                return

            reportlist = ReportList(self.id, self.position, REPORTHEADER[self.reqsection], self.reqsection)
            reportlist.run_screen()
    

    def report_choice(self):
        '''
        Prints out all report filters
        '''
        indentstring = '      '
        report_string = ''
        for index, word in enumerate(REPORTHEADER):
            report_string += f'{indentstring}{index+1}. {word.capitalize()}\n'
        report_string += f'{indentstring}{DASH*18}\n{indentstring}B. Back\n{STAR*20}'
        return report_string

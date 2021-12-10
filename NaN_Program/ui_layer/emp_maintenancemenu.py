#The maintenancemenu for an employee.
from data_files.const import CLEAR, INVALID, STAR, DASH, SLEEPTIME
from ui_layer.contractlist import ContractList
from ui_layer.reportlist import ReportList
from time import sleep
import os

class EmployeeMaintenanceMenu:
    def __init__(self, id, position) -> None:
        self.id = id
        self.position = position
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | MAINTENANCE |
        {DASH*15}
        1. My Requests
        2. My Reports
        {DASH*15}
        B. Til baka
{STAR*20}
        '''

    def display(self):
        while True:
            os.system(CLEAR)
            print(self.screen)
            user_input = input()

            if user_input == '1':
                empreport = ContractList(self.id, self.position, 'My Requests', 'employee', self.id)
                empreport.run_screen()

            elif user_input == '2':
                reportlist =  ReportList(self.id, self.position, 'My Reports', 'employee', self.id, True)
                reportlist.run_screen()

            elif user_input.upper() == 'B': 
                return

            else:
                print(INVALID) #if the user input is not one of the above, it is invalid.
                sleep(SLEEPTIME)
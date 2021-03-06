#velja ákveðinn starfsmann
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, REPORTTEMPLATE
from logic_layer.LLAPI import LLAPI


from time import sleep
import os



class SeeReport:
    def __init__(self, id, reportinfo, position) -> None:
        self.position = position
        self.llapi = LLAPI()
        self.id = id
        self.report = reportinfo
        editornot = ''
        if self.position == 'Manager' and (self.report['Status'] == '1' or self.report['Status'] == '2') :
            self.reportvar = 'PM' #PendingManager
            if self.report['Status'] == '1':
                editornot = f"\n\tC. Confirm"
            editornot += f"\n\tD. Deny"
        
        elif self.position == 'Employee' and self.report['Status'] == '0':
            self.reportvar = 'DE' #DeniedEmployee
            editornot = f"\n\tE. Edit & resubmit"
    
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position} 
{STAR*20}
          | MAINTENANCE |
          - Reportlist
            - {self.report['Title']}
        {DASH*15}{editornot}
        B. Back
'''

    def display(self):
        returnvalue = ''
        while returnvalue != 'B':
            self.reset_screen()
            returnvalue = self.prompt_user()

            if returnvalue == 'notpending':
                print('Changes saved')
                sleep(SLEEPTIME)
                return

    
    def printreportinfo(self, number = None):

        reportstring = f"{'| ' + self.report['Title'] + ' |':^70}\n{DASH*70}\n"

        for i in range(len(REPORTTEMPLATE)):
            if number != None and i == number - 1:
                reportstring += f"{i+1}. {REPORTTEMPLATE[i] + ':':<35} ____\n"
            else:
                reportstring += f"{i+1}. {REPORTTEMPLATE[i] + ':':<35} {self.report[REPORTTEMPLATE[i]]}\n"
        reportstring += DASH*70
        
        print(reportstring)
    
    
    def prompt_user(self, old_input = None):
        if old_input == None:
            user_input = input()
        else:
            user_input = old_input
        
        if user_input.upper() == 'B':
            return 'B'

        elif self.reportvar == 'PM':
            if user_input.upper() == 'C' and self.report['Status'] == '1':
                self.boss_feedback = input('Report feedback: ')
                self.report['Feedback'] = self.boss_feedback
                if self.report['Contractor-id'] != '':
                    valid = False
                    while not valid:
                        contractor_rating = input('Contractor Rating: ')
                        valid = self.validate_rating(contractor_rating)

                    self.report['Contractor-rating'] = contractor_rating
                self.report['Status'] = '2'
                self.llapi.confirm_or_deny_pending_report(self.report)
                return 'notpending'

            elif user_input.upper() == 'D':
                self.report['Status'] = '0'
                boss_feedback = input('Report feedback: ')
                self.report['Feedback'] = boss_feedback
                self.llapi.confirm_or_deny_pending_report(self.report)
                return 'notpending'

        elif self.reportvar == 'DE':
            if user_input.upper() == 'E':
                self.report['Status'] = '1'
                emp_description = input("Add description: ")
                self.report['Description'] = emp_description
                self.llapi.confirm_or_deny_pending_report(self.report)
                return 'notpending'
                

        print(INVALID)
        sleep(SLEEPTIME)


    def change_row(self, row = None):

        if row == None:
            user_row = None
            while user_row is None:
                self.reset_screen()
                user_input = input("Row to change: ")
                user_row = self.validate(user_input)
        else:
            user_row = row + 1
        self.reset_screen(user_row)

        user_input = input(f"{REPORTTEMPLATE[user_row - 1]}: ")
        old_input = self.report[REPORTTEMPLATE[user_row - 1]]
        self.report[REPORTTEMPLATE[user_row - 1]] = user_input 

        returnvalue = self.confirm_edit(old_input, user_row)
        if returnvalue == 'B' or returnvalue == 'C':
            return returnvalue
        elif returnvalue is not None: #here we know that the returnvalue is neither a 'B' or a 'C', therefore the self.confirm_edit(self) has denied the submission and returnes the invalid key.
            row = REPORTTEMPLATE.index(returnvalue)


    def confirm_edit(self, old_input, user_row):
        while True:
            self.reset_screen()
            is_user_happy = input("C. Confirm\nE. Edit\nB. Back\n")
                
            if is_user_happy.upper() == 'C':
                valid, key = self.llapi.edit_rep(self.report)
                if valid:
                    print("Changes saved!")
                    sleep(SLEEPTIME)
                    return 'C'
                else:
                    print(f"Invalid {key}!")
                    sleep(SLEEPTIME)
                    return key

            elif is_user_happy.upper() == 'B':
                self.report[REPORTTEMPLATE[user_row - 1]] = old_input
                return is_user_happy.upper()
            
            elif is_user_happy.upper() == 'E':
                return None

            else:
                print(INVALID)
                sleep(SLEEPTIME)
    

    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            if 1 <= rowint <= len(REPORTTEMPLATE):
                return rowint
            else:
                raise ValueError
        except ValueError:
            print(INVALID)
            sleep(SLEEPTIME)
            return None
        
    
    def validate_rating(self, user_input):
        if user_input.isdigit():
            if 0 <= int(user_input) <= 10:
                return True
        
        print(INVALID)
        sleep(SLEEPTIME)
        self.reset_screen()
        print(f'Report feedback: {self.boss_feedback}')
            
        return False


    def reset_screen(self, user_row = None):
        os.system(CLEAR)
        print(self.screen)
        self.printreportinfo(user_row)
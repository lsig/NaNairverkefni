#skrá nýja fasteign
from data_files.const import CLEAR, INVALID, SLEEPTIME, STAR, DASH, QUIT, CREATEREPORTTEMPLATE
import os 
from time import sleep
from logic_layer.LLAPI import LLAPI


class EmpReportCreate:
    def __init__(self, id, contractinfo) -> None:
        self.llapi = LLAPI()
        self.contract = contractinfo
        self.id = id
        self.reportdict = {}
        self.screen = f'''
 {self.id['Destination']} | {self.id['Name']} | Employee
{STAR*20}
          | MAINTENANCE |
          - Contractlist
            - Report: {self.contract['Title']}
        {DASH*15}
        {QUIT}. Quit / Cancel

'''



    def display(self):

        os.system(CLEAR)
        print(self.screen)

        print(f"{'| ' + self.contract['Title'] + ' |':^70}\n{DASH*70}")

        for i in range( len(CREATEREPORTTEMPLATE)): 
            user_input = input(f"{i+1}. {CREATEREPORTTEMPLATE[i] + ':':<35} ") #The user puts in info for every section of the contract
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return
            #check validity
            #while self.input_is_valid(user_input) == False:
                #user_input = input(f"{i+1}: {CREATEREPORTTEMPLATE[i]}")
            self.reportdict[CREATEREPORTTEMPLATE[i]] = user_input
        print(DASH*70)
        
        self.confirmcontract()

        
    def printcontractinfo(self, number = None):

        contractstring = f"{'| ' + self.contract['Title'] + ' |':^70}\n{DASH*70}\n"
        for i in range( len(CREATEREPORTTEMPLATE)):
            if number != None and i == number - 1:
                contractstring += f"{i+1}. {CREATEREPORTTEMPLATE[i] + ':':<35} ____\n"
            else:
                contractstring += f"{i+1}. {CREATEREPORTTEMPLATE[i] + ':':<35} {self.reportdict[CREATEREPORTTEMPLATE[i]]}\n"
        contractstring += DASH*70
        
        print(contractstring)
    
    #1:Kulsuk, 2:Þórshöfn, 3: longyearbyen
    def confirmcontract(self):

        while True:
            confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel\n""")

            if confirm.upper() == 'C':  # TODO
                #self.reportdict['Contractor-rating'] = '0'
                valid, key = self.llapi.create_report(self.reportdict, self.contract)
                #self.contract['Status'] = '1'
                
                if valid: 
                    new_report_dict = self.llapi.id_for_report_create(self.contract['id'])
                    new_report_dict['Status'] = '1'

                    self.llapi.confirm_or_deny_pending_report(new_report_dict)
                    print("Contract succesfully added!")
                    sleep(SLEEPTIME)
                    return
                else:
                    print(f"Wrong {key}")
                    sleep(SLEEPTIME)
                    self.editcontractinfo( CREATEREPORTTEMPLATE.index(key) )
        
            elif confirm.upper() == 'E': # TODO
                self.editcontractinfo()

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                sleep(SLEEPTIME)
                self.reset_screen()
    
    def editcontractinfo(self, row = None):
        if row == None:
            user_row = None
            while user_row is None:
                self.reset_screen()
                user_input = input("Row to change: ")
                user_row = self.validate(user_input)
        else:
            user_row = row + 1 
        self.reset_screen(user_row)

        user_input = input(f"{CREATEREPORTTEMPLATE[user_row - 1]}: ")
        self.reportdict[CREATEREPORTTEMPLATE[user_row - 1]] = user_input

        self.reset_screen()
    

    def validate(self, rowinput):
        try:
            rowint = int(rowinput)
            if 1 <= rowint <= len(CREATEREPORTTEMPLATE):
                return rowint
            else:
                raise ValueError
        except ValueError:
            print(INVALID)
            sleep(SLEEPTIME)
            return None
    
    
    def reset_screen(self, user_row = None):

        os.system(CLEAR)
        print(self.screen)
        self.printcontractinfo(user_row)

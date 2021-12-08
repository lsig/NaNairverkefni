#starfsmannalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
#from ui_layer.boss_seedestination import SeeDestination
from logic_layer.LLAPI import LLAPI
from time import sleep
import os
MAXROWS = 50
ROWS = 10
DESTPRINTER = [(4,'id'), (20,'SS'), (20,'Name'), (25, 'address') , (15, 'phone'), (15, 'GSM'), (25, 'email'), (20, 'destination'), (0,'other')]
DESTPRINT = [element[0] for element in DESTPRINTER]
SEARCHFILTERS = ['Name','Email','Destination', 'Social Security']


class DestinationList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = ROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.destinationlist = self.llapi.get_emp_info()
        self.destinationlist_backup = self.llapi.get_emp_info()
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | STARFSMENN |
     - Starfsmannalisti
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
            for index, k in enumerate(self.destinationlist[0].keys()):
                if k == 'id':
                    extra = '  '
                else:
                    extra = ''
                if k != 'Manager':# and k != 'Social Security':
                    print(f"{'| ' + k + extra:<{DESTPRINT[index]}}",end='')
            print(f"\n{DASH* sum(DESTPRINT) }")

            for i in range(self.rows): #ef að við displayum self.rows starfsmenn í röð.
                try:
                    destinationinfostr = f'{self.destinationlist[self.firstrow + i]["id"] + ".":<{DESTPRINT[0]}}- ' #id with some extra text.
                    for index, k in enumerate(self.destinationlist[self.firstrow + i]):
                        if k == 'Address': #the address in the csv file stores town and country, seperated by semicommas (;), we only want the house address.
                            infotoprint = self.destinationlist[self.firstrow + i][k].split(';')[0]
                            destinationinfostr += f"{'| ' + infotoprint[0:22] :<{DESTPRINT[index]}}"

                        elif k != 'id' and k != 'Manager':# and k != 'Social Security': #We dont want to print the id again, and we dont want to print the manager status and social security number at all.
                            destinationinfostr += f"{'| ' + self.destinationlist[self.firstrow + i][k][0:22] :<{DESTPRINT[index]}}"
                    print(destinationinfostr, end='') #here we print an destination's information.
                        
                except IndexError: #if the destination id cant be found within the self.firstrow + i to self.firstrow + self.rows + i range, we get an indexerror and print an empty line.
                    pass
                print()
            
            self.print_footer()
    
    def prompt_user(self, oldinput = None):
        if oldinput == None:
            user_input = input()
        else:
            user_input = oldinput
            print()

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.destinationlist):
            self.slide += 1

        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = self.validate(None, '/ROW')
        
        elif user_input.upper() == 'L': #TODO
            self.find_destination()
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðinn starfsmann
            self.lastrow = (self.slide + 1) * self.rows + 1
            
            if self.firstrow <= int(user_input) < self.lastrow and len(self.destinationlist) >= int(user_input):
                #destinationinfo = self.llapi.filter_destination_id(user_input, self.destinationlist) 
                #seeemp = SeeDestination(self.id, destinationinfo, self.position)
                #seeemp.display()
                pass
            
            else: 
                print("Invalid row, try again!")
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)

    def find_destination(self):
        for index, filter in enumerate(SEARCHFILTERS):
            print(f"{index + 1}: {filter}")
        if self.destinationlist != self.destinationlist_backup:
            print('R: Reset')
        userint = self.validate('userint')

        if userint == 'B':
            return 'B'
        elif userint == 'R':
            self.destinationlist = self.destinationlist_backup
            return
        key = SEARCHFILTERS[userint - 1]
        userstring = input(f"Search in {key.lower()}: ")

        #filteredlist = self.llapi.search_destination(userstring, self.destinationlist, key)

        # if filteredlist == False:
        #     print(f"The filter {key.lower()}: {userstring} did not match any result.")
        #     sleep(SLEEPTIME*3)
        # else:
        #     self.destinationlist = filteredlist
        

    def print_header(self):
        for index, k in enumerate(self.destinationlist[0].keys()):
            if k == 'id':
                extra = '   '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{DESTPRINT[index]}}",end='')
        print(f"\n{DASH* sum(DESTPRINT) }")
    

    def print_footer(self):
        dashlen = 21
        print(f"{DASH * sum(DESTPRINT)}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
            dashlen += 14
        if (self.slide + 1) * self.rows < len(self.destinationlist):
            print("n. Next - ", end='')
            dashlen += 10
        print(f"#. to Select Destination\n{DASH*dashlen}")
        


    def validate(self, userint = None, userrows = None):
        if userint is not None:
            while True:
                userint = input(" ")
                if userint.upper() == 'B':
                    return 'B'
                elif userint.upper() == 'R':
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
#starfsmannalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
#from ui_layer.boss_seedestination import SeeDestination
from logic_layer.LLAPI import LLAPI
from ui_layer.boss_seedest import SeeDestination
from time import sleep
import os
MAXROWS = 50
ROWS = 10
DESTPRINTER = [(4,'id'), (20,'Name'), (25, 'country') , (20, 'Airport'), (15, 'Phone'), (15, 'Working-hours'), (20, 'Manager'), (15,'Manager-id')]
DESTPRINT = [element[0] for element in DESTPRINTER]
SEARCHFILTERS = ['Name','Country','Manager', 'Phone']


class DestinationList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = ROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.destinationlist = self.llapi.get_dest_info()
        self.destinationlist_backup = self.llapi.get_dest_info()
        self.screen = f''' 
{self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*14}
    | DESTINATIONS |
     - Destinationlist
     {DASH*15}
     L. Look
     B. Back
     /row. Change row length

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
            self.print_header()

            self.printedids = [self.destinationlist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.destinationlist) > self.firstrow + i]
            

            for i in range(self.rows): #ef að við displayum self.rows starfsmenn í röð.
                try:
                    destinationinfostr = f'{self.printedids[i] + ".":<{DESTPRINT[0]}}- ' #id with some extra text.
                    for index, k in enumerate(self.destinationlist[self.firstrow + i]):
                        if k != 'id':
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
            returnvalue = self.find_destination()
            if returnvalue == 'B':
                return
        
        elif user_input.isdigit(): #TODO, hér selectum við ákveðinn starfsmann
            
            if user_input in self.printedids: #if the user input is the same as an id that is currently printed on the list
                destinationinfo = self.llapi.filter_loc_id(user_input, self.destinationlist)  #as lists are mutable, we want to put the original list into filter_property_id as otherwise we would risk altering the filtered list.
                seeemp = SeeDestination(self.id, destinationinfo, self.position) 
                seeemp.display()
                self.destinationlist = self.llapi.get_dest_info()
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

        elif userint == 'R' and self.destinationlist != self.destinationlist_backup:
            self.destinationlist = self.destinationlist_backup
            return

        key = SEARCHFILTERS[userint - 1]
        userstring = input(f"Search in {key.lower()}: ")

        filteredlist = self.llapi.search_destination(userstring, self.destinationlist, key)

        if filteredlist == False:
             print(f"The filter {key.lower()}: {userstring} did not match any result.")
             sleep(SLEEPTIME*3)
        else:
             self.destinationlist = filteredlist
        

    def print_header(self):
        for index, k in enumerate(self.destinationlist[0].keys()):
            if k == 'id':
                extra = '  '
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
                elif userint.upper() == 'R' and self.destinationlist != self.destinationlist_backup:
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
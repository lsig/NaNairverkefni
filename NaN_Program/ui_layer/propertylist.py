#fasteignalisti
from data_files.const import CLEAR, DASH, INVALID, SLEEPTIME, STAR 
from ui_layer.boss_seeproperty import SeeProperty
from time import sleep
import os
from logic_layer.LLAPI import LLAPI
MAXROWS = 50
ROWS = 10
SEARCHFILTERS = ['Destination', 'Type', 'Rooms', 'Property-number']

PROPPRINT = [4, 15, 25, 8, 8, 15, 19, 15]


class PropertyList: 
    def __init__(self, id, position) -> None:
        self.llapi = LLAPI()
        self.rows = ROWS
        self.slide = 0
        self.id = id
        self.position = position
        self.propertylist = self.llapi.get_prop_info()
        self.propertylist_backup = self.llapi.get_prop_info()
        if self.position == 'Employee':
            self.propertylist = self.llapi.search_property(self.id['Destination'], self.propertylist,'Destination' )
            self.propertylist_backup = self.llapi.search_property(self.id['Destination'], self.propertylist,'Destination' )
        self.screen = f''' 
 {self.id['Destination']} | {self.id['Name']} | {self.position}
{STAR*20}
          | PROPERTIES |
          - Propertylist
        {DASH*15}
        L. Look
        B. Back
        /row. Change row length

'''
    def run_screen(self):
        '''
        This function "initiats" the class  
        '''
        returnvalue = ''
        while returnvalue != 'B':
            self.display_list()
            returnvalue = self.prompt_user()

    def display_list(self):
        '''
        displays the list in an orderly manner
        '''
        self.firstrow = self.slide * self.rows 
        os.system(CLEAR)
        print(self.screen)
        self.print_header()

        self.printedids = [self.propertylist[self.firstrow + i]['id'] for i in range(self.rows) if len(self.propertylist) > self.firstrow + i]

        for i in range(self.rows): #til að displaya self.rows fasteignir í röð.
            try:
                propertyinfost = f'{self.printedids[i] + ".":<{PROPPRINT[0]}}- ' #id with some extra text.
                for index, k in enumerate(self.propertylist[self.firstrow + i]):

                    if k != 'id': #We dont want to print the id again.
                        propertyinfost += f"{'| ' + self.propertylist[self.firstrow + i][k] :<{PROPPRINT[index]}}"
                print(propertyinfost, end='') #here we print an employee's information.
                    
            except IndexError: #if the employee id cant be found within the self.firstrow + i to self.firstrow + self.rows + i range, we get an indexerror and print an empty line.
                pass
            print()
        
        self.print_footer()
    

    def prompt_user(self, oldinput = None):
        '''
        prompts the user for input 
        '''
        if oldinput == None:
            user_input = input()
        else:
            user_input = oldinput
            print()

        if user_input.upper() == 'P' and self.slide > 0:
            self.slide -= 1

        elif user_input.upper() == 'N' and (self.slide + 1) * self.rows < len(self.propertylist):
            self.slide += 1
        
        elif user_input.upper() == 'B':
            return 'B'

        elif user_input.upper() == '/ROW':
            self.rows = self.validate(None, '/ROW')
        
        elif user_input.upper() == 'L':
            returnvalue = self.find_property()
            if returnvalue == 'B':
                return
        
        elif user_input.isdigit():
            
            if user_input in self.printedids:
                propertyinfo = self.llapi.filter_property_id(user_input, self.propertylist) #as lists are mutable, we want to put the original list into filter_property_id as otherwise we would risk altering the filtered list.
                seeproperty = SeeProperty(self.id, propertyinfo, self.position)
                seeproperty.display()
                self.propertylist = self.llapi.get_prop_info()
                if self.position == 'Employee':
                    self.propertylist = self.llapi.search_property(self.id['Destination'], self.propertylist,'Destination' )
            else: 
                print(INVALID)
                sleep(SLEEPTIME)

        else:
            print(INVALID)
            sleep(SLEEPTIME)
        

    def find_property(self):
        '''
        takes search parameters sends it to the ll
        and gets back a updated list
        '''
        for index, filter in enumerate(SEARCHFILTERS):
            print(f"{index + 1}: {filter}")
        if self.propertylist != self.propertylist_backup:
            print('R: Reset')
        userint = self.validate('userint')

        if userint == 'B':
            return 'B'
        elif userint == 'R' and self.propertylist != self.propertylist_backup:
            self.propertylist = self.propertylist_backup
            return
        key = SEARCHFILTERS[userint - 1]
        userstring = input(f"Search in {key.lower()}: ")

        filteredlist = self.llapi.search_property(userstring, self.propertylist, key)

        if filteredlist == False:
            print(f"The filter {key.lower()}: {userstring} did not match any result.")
            sleep(SLEEPTIME*3)
        else:
            self.propertylist = filteredlist
        

    def print_header(self):
        '''
        prints the header 
        '''
        for index, k in enumerate(self.propertylist[0].keys()):
            if k == 'id':
                extra = '  '
            else:
                extra = ''
            print(f"{'| ' + k + extra:<{PROPPRINT[index]}}",end='')
        print(f"\n{DASH* sum(PROPPRINT) }")
    

    def print_footer(self):
        '''
        prints the footer 
        '''
        dashlen = 21
        print(f"{DASH * sum(PROPPRINT)}\n")
        if self.slide > 0:
            print("p. Previous - ", end='')
            dashlen += 14
        if (self.slide + 1) * self.rows < len(self.propertylist):
            print("n. Next - ", end='')
            dashlen += 10
        if len(self.propertylist) > 0:
            print(f"#. to Select Property\n{DASH*dashlen}")
        


    def validate(self, userint = None, userrows = None):
        '''
        validate various user inputs that are easy to spot
        '''
        if userint is not None:
            while True:
                userint = input(" ")
                if userint.upper() == 'B':
                    return 'B'
                elif userint.upper() == 'R' and self.propertylist != self.propertylist_backup:
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
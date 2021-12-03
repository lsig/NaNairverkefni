#skrá nýjan starfsmann
#þarf að importa klösum eins og employee


from data_files.const import CLEAR, INVALID, QUIT, STAR, DASH, SLEEPTIME
from time import sleep
import os
CONTACTTEMPLATE = ['Nafn', 'Kennitala', 'Heimilisfang', 'Heimasími', 'GSM símanúmer', 'Netfang', 'Áfangastaður', 'Yfirmaður']

class BossEmployeeCreate:
    def __init__(self, id) -> None:
        self.id = id
        self.contactlist = []
        self.screen = f'''
 Location | Name | {self.id} 
{STAR*14}
    | STARFSMENN |
     - Skrá nýja starfsmann
      {DASH*15}
    {QUIT}. Hætta við
        '''

    def display_menu(self):
        os.system(CLEAR)
        print(self.screen)

        for i in range( len(CONTACTTEMPLATE)): 
            user_input = input(f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} ") #The user puts in info for every section of the property
            if user_input.upper() == QUIT: #The program exits if the user inputs q, for quitting.
                return
            #check validity
            #while self.input_is_valid(user_input) == False:
                #user_input = input(f"{i+1}: {CONTACTTEMPLATE[i]}")
            self.contactlist.append(user_input)
        print(DASH*25)
        
        self.confirmcontact()

        
    def printcontactinfo(self, number = None):
        propertystring = ''
        for i in range( len(CONTACTTEMPLATE)):
            if number != None and i == number - 1:
                propertystring += f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} ____\n"
            else:
                propertystring += f"{i+1}. {CONTACTTEMPLATE[i] + ':':<17} {self.contactlist[i]}\n"
        propertystring += DASH*25
        
        print(propertystring)
    

    def confirmcontact(self):

        confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")
        while True:
            if confirm.upper() == 'C':  # TODO
                #Property(dest_info, address_info, size_info, room_info, type_info, prop_number, extras_info)
                return
        
            elif confirm.upper() == 'E': # TODO
                self.editcontactinfo()
                confirm = input("""\nC. Confirm \nE. Edit \nQ. Quit / Cancel \n""")

            elif confirm.upper() == 'Q': # eigum við að setja QUIT hér inn?
                return

            else:
                print(INVALID)
                confirm = input()
    
    def editcontactinfo(self):
        user_row = int(input("Row to change: "))
        self.reset_screen(user_row)

        user_input = input(f"{CONTACTTEMPLATE[user_row - 1]}: ")
        self.contactlist[user_row - 1] = user_input

        os.system(CLEAR)
        print(self.screen)
        self.printcontactinfo()
    
    def reset_screen(self, user_row):
        os.system(CLEAR)
        print(self.screen)
        self.printcontactinfo(user_row)



        




    
 
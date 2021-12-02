#skrá nýja fasteign
from data_files.const import CLEAR, STAR, DASH
import os 
from time import sleep
PROPERTYTEMPLATE = []

class BossPropertyCreate:
    def __init__(self, id) -> None:
        self.id = id
        self.screen = f'''
 Location | Name | {self.id} 
{STAR*14}
    | FASTEIGNIR |
     - Skrá nýja fasteign
      {DASH*15}
        '''


    def display(self):
        os.system(CLEAR)
        print(self.screen)
        dest_info = 'Location' #Viljum mögulegalíklega nota bara locationið hjá yfirmanninum.
        address_info = input("Address: ")

        size_info = input("Size (m^2): ")
        while size_info.isdigit() == False:
            size_info = input("Invalid input:\nSize: ")

        room_info = input("Rooms: ")
        while room_info.isdigit() == False:
            room_info = input("Invalid input:\nRooms: ")
            
        type_info = input("Type: ")
        prop_number = input("Property number: ") #þurfum að testa hvort það sé valid

        extras_info = input("Extras (n for None):")
        if extras_info.lower() == 'n' or extras_info.lower() == 'none':
            extras_info == None
        
        #Property(dest_info, address_info, size_info, room_info, type_info, prop_number, extras_info)



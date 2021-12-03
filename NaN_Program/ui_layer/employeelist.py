#starfsmannalisti
from data_files.const import DASH, STAR 
class EmployeeList: 
    def __init__(self, id) -> None:
        self.id = id
        self.employeelist = [['Jói','1303576040','8776545','joi@nanair.is'], \
            ['Spói','1403579040','8876545','spoi@nanair.is'], \
            ['Gói','0903576030','','Gói@nanair.is']]
        self.screen = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | STARFSMENN |
     - Starfsmannalisti
     {DASH*15}
Nafn | Sími | Netfang | Kennitala
      {DASH*15}


      B. Til baka
{STAR*14}
        '''
    
    def display_list(self):
        print(self.screen)
        for i in range(len(self.employeelist)):
            pass



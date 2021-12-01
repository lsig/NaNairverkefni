#verktakagluggi
from ui_layer.boss_contractorcreate import BossContractorCreate
STAR = '* '
DASH = '-'
class BossContractorMenu:
    def __init__(self, id):
        self.id = id
        self.options = f''' 

 Location | Name | {self.id} 
{STAR*14}
      {DASH*15}
      1. Skrá nýjan verktaka
      2. Verktakalisti
      {DASH*15}
      B. Til baka
{STAR*14}
        '''
    
    def display(self):
        while True:
            print(self.options)
            user_choice = input()
            if user_choice == '1':
                createcontractor = BossContractorCreate(self.id)
                createcontractor.display_contractormenu()
            elif user_choice == '2':
                contractor_list = ''
            elif user_choice.upper() == 'B':
                return
            else:
                print('Invalid choice, try again!')
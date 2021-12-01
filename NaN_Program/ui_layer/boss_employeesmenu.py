from ui_layer.boss_employeecreate import BossEmployeeCreate
#starfsmannagluggi
#Employee Main Menu 
STAR = '* '
DASH = '-'
class BossEmployeesMenu: 
    def __init__(self, id):
        self.id = id
        self.options = f''' 

 Location | Name | {self.id} 
{STAR*14}
      {DASH*15}
      1. Skrá nýjan starfsmann
      2. Starfsmannalisti
      {DASH*15}
      B. Til baka
{STAR*14}
        '''
    
    def display(self):
        while True:
            print(self.options)
            user_choice = input()
            if user_choice == '1':
                createemployee = BossEmployeeCreate(self.id)
                createemployee.display_menu()
            elif user_choice == '2':
                emp_list = ''
            elif user_choice.upper() == 'B':
                return
            else:
                print('Invalid choice, try again!')
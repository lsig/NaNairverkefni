#Employee Main Menu 
STAR = '* '
DASH = '-'
class EmployeeMenu: 
    def __init__(self, id):
        self.id = id
        self.options = f''' 

 Location | Name | {self.id} 
{STAR*14}
      {DASH*15}
      1. Fasteignir 
      2. Viðhald
      3. Verktakar
      {DASH*15}
{STAR*14}
        '''

    def print_menu(self):
        print(self.options)
        self.user_input()

    def user_input(self):
        while True:   
            user_choice = input()
            if user_choice == '1':
                prop_menu = ''
            elif user_choice == '2':
                maintnence_menu = ''
            elif user_choice == '3':
                contract_menu = ''
            else:
                print('Invalid choice, try again!')
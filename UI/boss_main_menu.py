#Employee Main Menu 
STAR = '* '
DASH = '-'
class Employee_Main: 
    def __init__(self):
        self.options = f''' Location| Name | Staff ID 
{STAR*14}
      {DASH*15}
      1. Fasteignir 
      2. Starfsmenn
      3. Viðhald
      4. Verktakar
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
                emp_menu = ''
            elif user_choice == '3':
                maintnence_menu = ''
            elif user_choice == '4':
                contract_menu = ''
            else:
                print('Invalid choice, try again!')
        

menu = Employee_Main()
menu.print_menu()
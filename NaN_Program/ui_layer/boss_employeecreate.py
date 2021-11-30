#skrá nýjan starfsmann
STAR = '* '
DASH = '-'
class BossEmployeCreate: 
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
        print(self.options)
    
    def user_input(self):
        while True:   
            user_choice = input()
            if user_choice == '1':
                new_emp = ''
            elif user_choice == '2':
                emp_list = ''
            elif user_choice == 'B':
                return
            else:
                print('Invalid choice, try again!')
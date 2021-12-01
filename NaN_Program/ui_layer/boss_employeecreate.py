#skrá nýjan starfsmann
#þarf að importa klösum eins og employee
STAR = '* '
DASH = '-'
class BossEmployeeCreate: 
    def __init__(self, id):
        self.id = id
        self.options = f''' 
 Location | Name | {self.id} 
{STAR*14}
        '''
    
    def display_menu(self):
        print(self.options)
        self.create_employee()
        return 

    def create_employee(self):
        name = input('Nafn starfsmanns: ')
        social_sec = input('Kennitala starfsmanns: ')
        address = input('Heimilisfang: ')
        phone = input('Heimasími: ')
        gsm =  input('GSM sími: ')
        email = input('Netfang: ')
        destination = input('Áfangastaður: ')
        manager = input('Yfirmaður: ')
        #new_employee = Employee(name,social_sec,address,phone,gsm,email,destination,manager)

        if True: #TODO
            return
    
 
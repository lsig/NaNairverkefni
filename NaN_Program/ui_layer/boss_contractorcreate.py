#skrá nýjan verktaka
STAR = '* '
DASH = '-'
class BossContractorCreate: 
    def __init__(self, id):
        self.id = id
        self.options = f''' 
 Location | Name | {self.id} 
{STAR*14}
    | VERKTAKAR |
     - Skrá nýjan verktaka
      {DASH*15}
        '''
    
    def display_contractormenu(self):
        print(self.options)
        self.create_contractor()
        return 

    def create_contractor(self):
        name = input('Nafn verktaka: ')
        contact_name = input('Kennitala starfsmanns: ')
        phone = input('Heimasími: ')
        work_hours =  input('GSM sími: ')
        location = input('Netfang: ')
        rating = input('Áfangastaður: ')
        #new_contractor = Contractor(name,contact_name,address,phone,work_hours,location,rating)

        if True: #TODO
            return
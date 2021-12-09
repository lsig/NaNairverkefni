import os 
if os.name == 'nt': #til að cleara terminal, hér er os-ið hjá notandanum windows
    CLEAR = 'cls'
else: # hér hlýtur os.name == 'posix', og os-ið hjá notandanum er mac eða linux.
    CLEAR = 'clear'

SLASH = os.sep
STAR = '* '
DASH = '-'
SLEEPTIME = 1 #var 1.5
INVALID = 'Invalid option, try again!'
QUIT = 'Q'

CONTACTTEMPLATE = ['Name', 'Social Security', 'Address', 'Phone', 'GSM', 'Destination'] #listi fyrir starfsmenn
CONTRACTTEMPLATE = ["Employee-id","Title","Description","Property-id","Priority(ASAP,Now,Emergency)","Suggested-contractor(id)"] #listi fyrir verkbeiðnir
REGCONTRACTTEMPLATE = CONTRACTTEMPLATE + ["Frequency(Week: 1, or Month: 2)", '"Date-to(dd-mm-yyyy)"']
PROPERTYTEMPLATE = ['Destination', 'Address', 'Size', 'Rooms', 'Type', 'Property-number', 'Extras'] # listi fyrir fasteignir
CONTRACTORTEMPLATE = ["Name","Contact-name","Profession","Phone","Working-hours","Location"] #listi fyrir verktaka
DESTINATIONTEMPLATE = ['Name', 'Country' ,'Airport', 'Phone', 'Working-hours', 'Manager', 'Social Security', 'Address', 'Phone-manager', 'GSM']
REPORTTEMPLATE = ['Report-id', 'Request-id', 'Employee', 'Employee-id', 'Title', 'Description', 'Location', 'Property', 'Property-number', 'Property-id', 'Contractor-name', 'Contractor-id', 'Contractor-rating', 'Date', 'Commission', 'Status']




# CONTRACTORTEMPLATE = ['Nafn verktaka', 'Nafn tengiliðs','Nafn sérhæfingu', 'Sími', 'Opnunartími','Áfangastaður'] #listi fyrir verktaka
#PROPERTYTEMPLATE = ['Áfangastaður', 'Heimilisfang', 'Stærð', 'Herbergi', 'Tegund', 'Númer fasteignar', 'Auka'] # listi fyrir fasteignir
#CONTRACTTEMPLATE = ['Stofnun verkbeiðnar','Starfsmaður', 'Starfsmanna ID', 'Titill', 'Lýsing', 'Áfangastaður', 'Fasteign', 'Númer fasteignar', 'Fasteignar ID', 'Forgangur','Staða'] #listi fyrir verkbeiðnir
# CONTACTTEMPLATE = ['Nafn', 'Kennitala', 'Heimilisfang', 'Heimasími', 'GSM símanúmer', 'Netfang', 'Áfangastaður', 'Yfirmaður'] #listi fyrir starfsmenn

if __name__ == '__main__':
    pass
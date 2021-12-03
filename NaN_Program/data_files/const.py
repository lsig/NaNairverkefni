import os 
if os.name == 'nt': #til að cleara terminal, hér er os-ið hjá notandanum windows
    CLEAR = 'cls'
else: # hér hlýtur os.name == 'posix', og os-ið hjá notandanum er mac eða linux.
    CLEAR = 'clear'

STAR = '* '
DASH = '-'
SLEEPTIME = 1.5
INVALID = 'Invalid option, try again!'
QUIT = 'Q'

CONTACTTEMPLATE = ['Nafn', 'Kennitala', 'Heimilisfang', 'Heimasími', 'GSM símanúmer', 'Netfang', 'Áfangastaður', 'Yfirmaður'] #listi fyrir starfsmenn
CONTRACTTEMPLATE = ['Stofnun verkbeiðnar','Starfsmaður', 'Starfsmanna ID', 'Titill', 'Lýsing', 'Áfangastaður', 'Fasteign', 'Númer fasteignar', 'Fasteignar ID', 'Forgangur','Staða'] #listi fyrir verkbeiðnir
PROPERTYTEMPLATE = ['Áfangastaður', 'Heimilisfang', 'Stærð', 'Herbergi', 'Tegund', 'Númer fasteignar', 'Auka'] # listi fyrir fasteignir
CONTRACTORTEMPLATE = ['Nafn verktaka', 'Nafn tengiliðs', 'Sími', 'Opnunartími','Áfangastaður', 'Einkunn'] #listi fyrir verktaka

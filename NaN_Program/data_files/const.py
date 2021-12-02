import os 
if os.name == 'nt': #til að cleara terminal, hér er os-ið hjá notandanum windows
    CLEAR = 'cls'
else: # hér hlýtur os.name == 'posix', og os-ið hjá notandanum er mac eða linux.
    CLEAR = 'clear'

STAR = '* '
DASH = '-'
SLEEPTIME = 1.5
INVALID = 'Invalid option, try again!'



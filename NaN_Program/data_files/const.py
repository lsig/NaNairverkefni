import os 
if os.name == 'nt': #til að cleara terminal, hér er os-ið hjá notandanum windows
    CLEAR = 'cls'
else: # hér hlýtur os.name == 'posix', og os-ið hjá notandanum er mac eða linux.
    CLEAR = 'clear'

SLASH = os.sep
STAR = '* '
DASH = '-'
SLEEPTIME = 1 
INVALID = 'Invalid option, try again!'
QUIT = 'Q'

#Templates for working with different aspects of the program

CONTACTTEMPLATE = ['Name', 'Social Security', 'Address', 'Phone', 'GSM', 'Destination'] #listi fyrir starfsmenn
CONTRACTTEMPLATE = ["Employee-id", "Title", "Description", "Property-id", "Priority(ASAP; Now; Emergency)", "Suggested-contractor(id)"] #listi fyrir verkbeiðnir
REGCONTRACTTEMPLATE = CONTRACTTEMPLATE + ["Frequency(Week: 1, or Month: 2)", "Date-to(dd-mm-yyyy)"]
PROPERTYTEMPLATE = ['Destination', 'Address', 'Size', 'Rooms', 'Type', 'Property-number', 'Extras'] # listi fyrir fasteignir
CONTRACTORTEMPLATE = ["Name","Contact-name","Profession","Phone","Working-hours"] #listi fyrir verktaka, location kemur frá boss
DESTINATIONTEMPLATE = ['Name', 'Country' ,'Airport', 'Phone', 'Working-hours', 'Manager', 'Social Security', 'Address', 'Phone-manager', 'GSM']
REPORTTEMPLATE = ['Report-id', 'Request-id', 'Employee', 'Employee-id', 'Title', 'Description', 'Location', 'Property', 'Property-number', 'Property-id', 'Contractor-name', 'Contractor-id', 'Contractor-rating', 'Date', 'Commission', 'Status', 'Feedback']

CREATEREPORTTEMPLATE = ['Description', 'Contractor-id', 'Commission','Total-cost']

JOBDICT = {'id': 5, 'Date-created': 15, 'Employee': 20, 'Title': 25, 'Location': 20, 'Property': 25, 'Priority(ASAP; Now; Emergency)': 12, 'Suggested-contractors': 30, 'Status':10,  'Type': 15}
REPORTDICT = {'Report-id': 5, 'Employee': 20, 'Title': 25, 'Location': 20, 'Property': 25, 'Contractor-rating': 10, 'Date': 15, 'Commission': 15, 'Status': 10}

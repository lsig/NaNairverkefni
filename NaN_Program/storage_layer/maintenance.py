class Maintenance:
    def __init__(self,id,Date_from,Date_to,Title,Description,Location,Property,Property_number,Property_id,Employee,Employee_id,Frequency,Priority,Suggested_contractors):
        self.id = id
        self.date_from = Date_from
        self.date_to = Date_to
        self.title = Title
        self.description = Description
        self.loc = Location
        self.property = Property
        self.property_num = Property_number
        self.property_id = Property_id
        self.emp = Employee
        self.emp_id = Employee_id
        self.freq = Frequency
        self.priority = Priority
        self.suggested_cont = Suggested_contractors

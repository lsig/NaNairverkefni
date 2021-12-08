class Maintenance:
    def __init__(self,id,Date_from,Date_to,Frequency,Employee,Employee_id,Title,Description,Location,Property,Property_number,Property_id,Priority,Suggested_contractors_names,Suggested_contractors_id,Status):
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
        self.suggested_cont_names = Suggested_contractors_names
        self.suggested_cont_id = Suggested_contractors_id
        self.status = Status

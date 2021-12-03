class Employee:
    def __init__(self, name, id, datecreated, description, location, property, propertynumber, priority, status)
        self.name = name
        self.id = id
        self.datecreated = datecreated
        self.description = description
        self.location = location
        self.property = property
        self.propertynumber = propertynumber
        self.priority = priority
        self.status = status
    
    def __str__(self):
        return f"name: {self.name}, id: {self.id}, date created: {self.datecreated}, description: {self.description}, location: {self.location}, property: {self.property}, property number: {self.propertynumber}, priority: {self.priority}, status: {self.status}"
        

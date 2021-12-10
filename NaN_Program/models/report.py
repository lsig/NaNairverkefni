from datetime import date


class Report:
    def __init__(self,report_id,request_id,emp,emp_id,title,descript,location,property,property_number,property_id,contract_name,contract_id,contract_rating,date,commission,cost,status,feedback):
        self.report_id = report_id
        self.request_id = request_id
        self.emp = emp
        self.emp_id = emp_id
        self.title = title
        self.descript = descript
        self.loc = location
        self.prop = property
        self.prop_nr = property_number
        self.prop_id = property_id
        self.contract_name = contract_name
        self.contract_id = contract_id
        self.contract_rating = contract_rating
        self.date = date
        self.comm = commission
        self.total = cost
        self.status = status
        self.feed = feedback
        


    
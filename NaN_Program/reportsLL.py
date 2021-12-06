from storage_layer.DLAPI import DlAPI
from models.report import Report
from datetime import datetime

class ReportsLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_report(self, rep_dic,job_dic):
        if self.is_valid(rep_dic):
            current_date = datetime.date(datetime.now())
            rep_dic = self.replace_loc_num_with_name(rep_dic)
            rep = Report(self.new_id(), job_dic["id"],job_dic["Employee"],job_dic["Employee-id"],rep_dic["Title"],rep_dic["Description"],rep_dic["Contractor-name"], rep_dic["Contractor-id"], None, current_date, "0")
            self.dlapi.add_report(rep)
            return True
        return False

    def generate_id(self):
        all_rep_lis = self.dlapi.get_all_report()
        new_id = int(all_rep_lis[len(all_rep_lis)-1]["id"])+1
        return new_id

    def list_all_reports(self):
        all_rep = self.dlapi.get_all_report()
        return all_rep


    def report_validation(self, rep_dic):
        dic = {"Title":str, "Description":"both", "Contractor-name":str, "Contractor-id":int}
        counter = 0
        for key in dic.keys():
            if dic[key] == str and dic[key] != "both":
                get_validation = rep_dic[key].replace(" ", "").isalpha()
            elif dic[key] == int and dic[key] != "both":
                get_validation = rep_dic[key].isdigit()
            if dic[key] == "both":
                if rep_dic[key] == "":
                    return False


        
         
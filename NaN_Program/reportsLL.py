from storage_layer.DLAPI import DlAPI
from models.report import Report
from datetime import datetime

# NOTETOSELF - sum verk krefjast verktaka, en ekki öll. Td gluggaþvottur krefst ekki en að laga pípulagnir krefst þess. 
# Ef verktaki er nauðsynlegur, þarf að taka fram þóknun verktaka, en ekki þarf að gera það ef enginn verktaki er ráðinn.

class ReportsLL:
    def __init__(self):
        self.dlapi = DlAPI()

    def add_report(self, rep_dic,job_dic):
        if self.is_valid(rep_dic):
            current_date = datetime.date(datetime.now())
            rep_dic = self.replace_loc_num_with_name(rep_dic)
            rep = Report(self.new_id(), job_dic["id"],job_dic["Employee"],job_dic["Employee-id"],rep_dic["Title"],rep_dic["Description"],rep_dic["Contractor-name"], rep_dic["Contractor-id"], None, current_date, rep_dic["Commission"], "0")
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

    def edit_report_info(self, edit_rep_dic):
        # NOTETOSELF:yfirmaður þarf að geta samþykkt viðhaldsskýrslur, og starfsmenn þurfa að geta séð hvaða skýrslur, sem þeir eiga, eru samþykktar og hverjar ekki.
        # Ef skýrsla er ekki samþykkt, þarf starfsmaður að geta breytt upplýsingum í skýrslunni.
        if self.report_validation(edit_rep_dic):
            all_list_rep = self.dlapi.get_all_report()

        # NOTETOSELF: Skýrslur merktar "pending", "accepted", eða "rejected"
        # yfirmaður getur merkt skýrslu accepted eða rejected, en starfsmaður getur merkt skýrslu pending.
        # # # 

    def report_validation(self, rep_dic, cont_dic):
        # a dictionairy for title, description, contractor-name and contractor-id.
        dic = {"Title":str, "Description":"both", "Contractor-id":int, "Commission": int}
        counter = 0
        prev = 0
        for key in dic.keys():
            if key == "Commission":
                if prev != "" and rep_dic[key] == "" or prev == "" and rep_dic[key] != "":
                    return False, key                
            # checking if the dictionairy key is a string and not both string and integer, and if so, remove spaces.
            if dic[key] == str and dic[key] != "both":
                get_validation = rep_dic[key].replace(" ", "").isalpha()
            # checking if the dictionairy key is an integer and not both string and integer, and if so, check if integer is in fact a number/digit.
            elif dic[key] == int and dic[key] != "both" and rep_dic[key] != "":
                get_validation = rep_dic[key].isdigit()
            # checking if the dictionairy key is both a string and integer, and if so, check if the key is empty. If so, the program will return False.
            if dic[key] == "both":
                if rep_dic[key] == "":
                    return False, key
            if get_validation == False:
                    return False, key
            prev = rep_dic[key]
            return True

        
if __name__ == "__main__":
    r = ReportsLL()
    r.add_report

        
         
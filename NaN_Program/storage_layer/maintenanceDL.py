import csv
from os import sep
# from maintenance import Maintenance
class MaintenanceDL():
    def __init__(self):
        self.csv = f"CSV_Files{sep}Regular_maintenance.csv"


    def get_all_maintenance_jobs(self):
        ret_lis = []
        with open(self.csv, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_dict = {}
                for item in row:
                    temp_dict[item] = row[item]
                ret_lis.append(temp_dict)
        return ret_lis

    def add_maintenance_job(self,main_job):
        with open(self.csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["id","Date-from","Date-to","Title","Description","Location","Property","Property-number","Property-id","Employee","Employee-id","Frequency","Priority","Suggested-contractor"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({"id":main_job.id,"Date-from":main_job.date_from,"Date-to":main_job.date_to,"Title":main_job.title,"Description":main_job.description,
            "Location":main_job.loc,"Property":main_job.property,"Property-number":main_job.property_num,
            "Property-id":main_job.property_id,"Employee":main_job.emp,"Employee-id":main_job.emp_id,"Frequency":main_job.freq,"Priority":main_job.priority,"Suggested-contractor":main_job.suggested_cont})

    
    def change_maintenance_job_info(self,rep_lis):
         with open("test.csv", 'w+', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            header = rep_lis[0]
            writer.writerow(header)
            for dic in rep_lis:
                writer.writerow([dic["id"],dic["Date-to"],dic["Date-from"],dic["Title"],
                dic["Description"],dic["Location"],dic["Property"],dic["Property-number"]
                ,dic["Property-id"],dic["Employee"],dic["Employee-id"],dic["Frequency"],dic["Priority"],dic["Suggested-contractor"]])


if __name__ == "__main__":
    g = MaintenanceDL()
    t = Maintenance("1","10","20","þrif","þarf að þrýfa húsið","nuuk","siggastaðir","20","50","Haraldur","23","7","High","Arnar, guðni, Ármann")
    g.add_maintenance_job(t)
    g.change_maintenance_job_info(g.get_all_maintenance_jobs())
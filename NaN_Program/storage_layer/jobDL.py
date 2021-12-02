import csv
from job import Job

class JobDL:
    def __init__(self):
        self.csv = "CSV_Files/Maintenance_request.csv"

    def get_all_jobs(self):
        ret_lis = []
        with open(self.csv, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_dict = {}
                for item in row:
                    temp_dict[item] = row[item]
                    # print(item,row[item])
                ret_lis.append(temp_dict)
        return ret_lis

    def add_job(self,jobinfo):
        with open(self.csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["id","Date-created","Employee","Employee-id","Title","Description","Location","Property","Property-number","Property-id","Priority","Suggested-contractors","Status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': jobinfo.id, "Date-created": jobinfo.date_cr, "Employee": jobinfo.empl, "Employee-id": jobinfo.empl_id,"Title":jobinfo.titl, "Description": jobinfo.desc, "Location": jobinfo.loc,"Property":jobinfo.prop, "Property-number":jobinfo.prop_num,"Property-id":jobinfo.prop_id,"Priority":jobinfo.prior,"Suggested-contractors":jobinfo.sug_con,"Status":jobinfo.stat})


    def change_job_info(self,job_lis):
        with open(self.csv, 'w+', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            header = job_lis[0]
            writer.writerow(header)
            for dic in job_lis:
                writer.writerow([dic["id"],dic["Date-created"],dic["Employee"],dic["Employee-id"],dic["Title"],dic["Description"],dic["Location"],dic["Property"],dic["Property-number"],dic["Property-id"],dic["Priority"],dic["Suggested-contractors"],dic["Status"]])
        
            




if __name__ == "__main__":
    g = JobDL()
    lis = g.get_all_jobs()
    #jobinfo = Job("1","0","John","1","Clean!","Clean oven","Something","something2","1111","1","High","1","0")
    #g.add_job(jobinfo)
    g.change_job_info(lis)
        
import csv
# from report import Report
class ReportDL():
    def __init__(self):
        self.csv = "CSV_Files\Reports.csv"


    def get_all_reports(self):
        ret_lis = []
        with open(self.csv, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_dict = {}
                for item in row:
                    temp_dict[item] = row[item]
                ret_lis.append(temp_dict)
        return ret_lis

    def add_report(self,rep):
        with open(self.csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Report-id","Request-id","Employee","Employee-id","Title","Description","Contractor-name","Contractor-id","Contractor-rating","Status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({"Report-id":rep.report_id,"Request-id":rep.request_id,"Employee":rep.emp,"Employee-id":rep.emp_id,"Title":rep.title,"Description":rep.descript,
            "Contractor-name":rep.contract_name,"Contractor-id":rep.contract_id,"Contractor-rating":rep.contract_rating,"Status":rep.status})

    
    def change_report_info(self,rep_lis):
         with open(self.csv, 'w+', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            header = rep_lis[0]
            writer.writerow(header)
            for dic in rep_lis:
                writer.writerow([dic["Report-id"],dic["Request-id"],dic["Employee"],dic["Employee-id"],
                dic["Title"],dic["Description"],dic["Contractor-name"],dic["Contractor-id"],dic["Contractor-rating"],dic["Status"]])


if __name__ == "__main__":
    g = ReportDL()
    t = Report("1","1","Siggi","0","Gluggar","þarf að þrýfa, glugganga","Haraldur","smiður","7","óklárað")
    g.add_report(t)
    g.change_report_info(g.get_all_reports())
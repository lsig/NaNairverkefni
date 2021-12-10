import csv
from os import sep


class ContractorDL:
    def __init__(self):
        self.csv = f"CSV_Files{sep}Contractor.csv"

    def get_all_contractor(self):
        ''' this function lists dicts of all reports from in a csv file
        '''
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

    def add_contractor(self,con):
        ''' this function adds contractor to a csv file
        '''
        with open(self.csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["id","Name","Contact-name","Profession","Phone","Working-hours","Location","Rating(0-10)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': con.id, "Name": con.name, "Contact-name": con.cont_name,"Profession":con.profess, "Phone": con.phone, "Working-hours": con.work_h, "Location": con.loc,"Rating(0-10)":con.rating})

    def change_con_info(self,con_lis):
        ''' This function edits the csv file if something is edited
        '''
        with open(self.csv, 'w+', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            header = con_lis[0]
            writer.writerow(header)
            for dic in con_lis:
                writer.writerow([dic["id"],dic["Name"],dic["Contact-name"],dic["Profession"],dic["Phone"],dic["Working-hours"],dic["Location"],dic["Rating(0-10)"]])
        
            




if __name__ == "__main__":
    g = ContractorDL()
    #lis = g.get_all_contractor()
    #print(lis[0])
    #con = Contractor("3","siggi","Johnny beep","6666669","00","Kulusuk","6")
    #g.add_contractor(con)
    #g.change_con_info(lis)
    
        
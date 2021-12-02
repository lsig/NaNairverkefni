import csv
# from location import Location
class LocationDL():
    def __init__(self):
        self.csv = "CSV_Files\Destination.csv"


    def get_all_loc(self):
        ret_lis = []
        with open(self.csv, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_dict = {}
                for item in row:
                    temp_dict[item] = row[item]
                ret_lis.append(temp_dict)
        return ret_lis

    def add_loc(self,loc):
        with open(self.csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Name","Country","Airport","phone","working-hours","Manager","Manager_id"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Name': loc.name, "Country": loc.country, "Airport": loc.airport, "phone": loc.phone, "working-hours": loc.work_time, "Manager": loc.manager,"Manager_id":loc.manager_id})

    
    def change_loc_info(self,loc_lis):
         with open("test.csv", 'w+', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            header = loc_lis[0]
            writer.writerow(header)
            for dic in loc_lis:
                writer.writerow([dic["Name"],dic["Country"],dic["Airport"],dic["phone"],dic["working-hours"],dic["Manager"],dic["Manager_id"]])


if __name__ == "__main__":
    g = LocationDL()
    t = Location("Reykjavík","iceland","NAN","00","00","Arnar Singh","1")
    # g.add_loc(t)
    g.change_loc_info(g.get_all_loc())
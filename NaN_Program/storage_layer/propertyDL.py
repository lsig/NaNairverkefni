import csv
from os import sep


class PropertyDL:
    def __init__(self):
        self.csv = f"CSV_Files{sep}Property.csv"

    def get_all_property(self):
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

    def add_property(self,prop):
        ''' this function adds property to a csv file
        '''
        with open(self.csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["id","Destination","Address","Size","Rooms","Type","Property-number","Extras"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'id': prop.id, "Destination": prop.dest, "Address": prop.addr, "Size": prop.size, "Rooms": prop.rooms, "Type": prop.typeOf,"Property-number":prop.propNum, "Extras":prop.extras})

    def change_prop_info(self,prop_lis):
        ''' This function edits the csv file if something is edited
        '''
        with open(self.csv, 'w+', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            header = prop_lis[0]
            writer.writerow(header)
            for dic in prop_lis:
                writer.writerow([dic["id"],dic["Destination"],dic["Address"],dic["Size"],dic["Rooms"],dic["Type"],dic["Property-number"],dic["Extras"]])
        
            




#if __name__ == "__main__":
    #g = PropertyDL()
    #lis = g.get_all_property()
    #prop = Property("31","lol","oll","100","6","Snowhouse","lol11","snowhouse")
    #g.add_property(prop)
    #g.change_prop_info(lis)
    
        
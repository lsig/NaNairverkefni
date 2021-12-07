from models.maintenance import Maintenance
from storage_layer.DLAPI import DlAPI


class MaintenanceLL:
    def __init__(self):
        self.dlapi = DlAPI()


    def add_maintenance(self,main_dic):
        pass


    def assign_id(self):
        all_main_job = self.dlapi.get_maintenance_jobs()
        if all_main_job != []:
            for dic in all_main_job:
                


        return 1
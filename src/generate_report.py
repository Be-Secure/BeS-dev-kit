from src.osspoi.osspoi_master_report import osspoiMaster
from src.osspoi.version_detail_report import osspoiVersionDetails

class GenerateReport:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
    
    def osspoiMasterReport(self):
        return osspoiMaster.createJsonForOsspoiMaster(self.name, self.id)


    
    def osspoiVersionReport(self):
        return osspoiVersionDetails.osspoiVersionDetailReport(self.id)
    
generateReport = GenerateReport
    
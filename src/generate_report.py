from src.osspoi.osspoi_master_report import osspoiMaster
from src.osspoi.version_detail_report import osspoiVersionDetails
from src.codeQL.codeql_report import codeQlReport

class GenerateReport:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
    
    def osspoiMasterReport(self, besecureOsspoi):
        return osspoiMaster.createJsonForOsspoiMaster(self.name, self.id, besecureOsspoi)

    def osspoiVersionReport(self, besecureOsspoi):
        return osspoiVersionDetails.osspoiVersionDetailReport(self.id, self.name, besecureOsspoi)
    
    def codeQlReport(self, ghtoken, besecureAssessment):
        return codeQlReport.codeQl_report(self.name, self.id, ghtoken, besecureAssessment)

    
generateReport = GenerateReport
    
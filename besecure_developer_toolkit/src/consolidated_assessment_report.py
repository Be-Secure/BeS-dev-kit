'''
    utility for generate 
    assessment report summary
'''
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from besecure_developer_toolkit.src.Scorecard_report import scorecard
from besecure_developer_toolkit.src.Sbom_report import sbom
from besecure_developer_toolkit.src.License_compliance import fossology
from besecure_developer_toolkit.src.Static_code_analysis import sonarqube
from besecure_developer_toolkit.src.Objective import objective

class Generate_report():

    def generate_report(self):
        obj = objective(self.OSSP_Name, self.version)
        elem1 = scorecard(self.OSSP_Name, self.version)
        elem2 = sbom(self.OSSP_Name, self.version)
        elem3 = fossology(self.OSSP_Name, self.version)
        elem4 = sonarqube(self.OSSP_Name, self.version)
        pdf = obj + elem1 + elem2 + elem3 + elem4
        return pdf

    def download_pdf(self, name, version):
        self.OSSP_Name = name
        self.version = version
        elems = self.generate_report()
        fileName = self.OSSP_Name+\
        '-'+self.version+'-'\
        'assessment-report.pdf'
        left_margin = 50
        right_margin = 50
        top_margin = 50
        bottom_margin = 50
        pdf = SimpleDocTemplate(
        fileName,
        pagesize=letter,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
        )
        pdf.build(elems)


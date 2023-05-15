from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.platypus.flowables import HRFlowable, ListFlowable
from reportlab.lib import colors

def objective(OSSP_name, version):
    '''add Objective of ossp'''
    #data
    desc1 = 'One key concern in the '\
        'open source software is often'\
        ' the security vulnerability and '\
        'operational risk. As part of the'\
        ' code readiness for '+OSSP_name+''\
        ' (Version: '+version+'), below '\
        'industry recommended assessments '\
        'are done on source code '\
        'of '+OSSP_name+' (Version: '+version+')'\
        ' to understand where does it stand in'\
        ' terms of code level risk.'
    desc2 = 'The outcome of the risk '\
        'assessment outlines the below '\
        'listed risk parameters '\
        'of '+OSSP_name+' (Version:'\
        ' '+version+') source code.'
    bullet_items1= [
        'Static Application Security Testing (SonarQube)',
        'Risk Criticality Assessment (OpenSSF Scorecard and OpenSSF Criticality Score)',
        'Software bill of materials (sbom-spdx-generator)',
        'License Compliance (Fossology)'
    ]
    bullet_items2 = [
        'Critical, High, Medium and Low severity vulnerabilities', 
        'Code smells and security hotspots', 
        'Dependency review that draw attention to the known risks in the dependent components', 
        'Risk criticality score ',
        'Incompatible licenses in the source code' 
    ]
    # Style
    desc_style = ParagraphStyle(
        name = "Description",
        fontName='Helvetica',
        fontSize=11,
        leading=12)
    heading_style = ParagraphStyle(
        name='Heading1',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=24,
        textColor=HexColor('#23395d'))
    bullet_style = ParagraphStyle(
        name='Bullet',
        bulletIndent=0.25*inch,
        leftIndent=0*inch,
        bulletFontSize=12,)
    line = HRFlowable(width="100%", thickness=2, 
                      lineCap='round', color=colors.ReportLabFidBlue,
                      spaceBefore=0, spaceAfter=15)
    # Create a list flowable with bullet points
    bullet_list_1 = ListFlowable([Paragraph(item, bullet_style) for item in bullet_items1],
                            bulletType='bullet', spaceBefore=12, spaceAfter=12)
    bullet_list_2 = ListFlowable([Paragraph(item, bullet_style) for item in bullet_items2],
                            bulletType='bullet', spaceBefore=12, spaceAfter = 12)
    # Add a heading to the document
    objective_heading = '<b>1. Objective</b>'
    objective_heading = Paragraph(objective_heading, heading_style)
    assessment_heading = '<b>2. Assessment Report</b>'
    assessment_heading = Paragraph(assessment_heading, heading_style)
    desc1 = Paragraph(desc1,desc_style)
    desc2 = Paragraph(desc2, desc_style)
    obj = [
        objective_heading,
        line, desc1,
        bullet_list_1,
        desc2,
        bullet_list_2,
        assessment_heading,
        line
    ]
    return obj

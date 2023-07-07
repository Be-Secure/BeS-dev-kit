import json, requests
from reportlab.platypus import Paragraph, Table
from reportlab.lib.pagesizes import mm
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
import sys
from rich import print
from bes_dev_kit.src.risk_summary.New_line_char import insert_newline_char

def scorecard(ossp_name, version):
    '''return pdf elements of Scorecard'''
    resp = getApiData(ossp_name, version)
    data = []
    data.append(["Name","Score","Reason"])
    for obj in resp["checks"]:
        sublist = []
        sublist.append(obj["name"])
        if "score" in obj:
            sublist.append(obj["score"])
        else:
            sublist.append("Not Available")
        reason = insert_newline_char(obj["reason"], 40, ' ')
        sublist.append(reason)
        data.append(sublist)
    data2 = [
        ['Score', 'Risk Category'],
        [10, 'Critical Risk'],
        [7.5, 'High Risk'],
        [5, 'Medium Risk'],
        [2.5, 'Low Risk']
    ]
    table1 = Table(data, colWidths=(50*mm, 30*mm, 100*mm), repeatRows=1)
    table1 = getTableStyle(table1, len(data))
    table2 = Table(data2, colWidths=(20*mm, 40*mm), repeatRows=1)
    table2 = getTableStyle(table2, len(data2))
    desc_style = ParagraphStyle(
        name='descStyle',
        leading=12,
        spaceAfter = 0,
        spaceBefore = 15
    )
    desc = getDesc(
        resp['repo']['name'],
        resp['score'],
        desc_style
    )
    scorecard_heading = getHeading()
    tool_desc = '<b>Tool: OpenSSF Scorecard</b>'\
        ' checks for vulnerabilities affecting'\
        ' different parts of the software supply'\
        ' chain including source code, build, '\
        'dependencies, testing and project '\
        'maintenance. This score helps give a '\
        'sense of the overall security posture '\
        'of a project as below.'
    tool_desc = Paragraph(tool_desc, desc_style)
    pages = [
        scorecard_heading,
        desc,
        table1,
        tool_desc,
        table2
    ]
    return pages

def getApiData(ossp_name, version):
    '''return data of API call'''
    try:
        url = 'https://raw.githubusercontent.com/Be-Secure/'\
            'besecure-assessment-datastore/main/'\
            +ossp_name+'/'+version+\
            '/scorecard/'\
            +ossp_name+'-'+version+\
            '-scorecard-report.json'
        resp = requests.get(url,  timeout=5)
    except requests.exceptions.HTTPError:
        print("HTTP Error")
        sys.exit(1)
    except requests.exceptions.ReadTimeout:
        print("Time out")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Connection error")
        sys.exit(1)
    except requests.exceptions.RequestException:
        print("Exception request")
        sys.exit(1)
    if resp.text == '404: Not Found':
        print(f'[bold red]Alert! [green]Invalid'+
              ' input or Scorecard'+
              ' report not available for', ossp_name)
        sys.exit(1)
    resp = json.loads(resp.text)
    return resp

def getTableStyle(table, length):
    '''return table style of Scorecard checks'''
    style = TableStyle([
    ('BACKGROUND', (0,0), (3,0), colors.ReportLabBlueOLD),
    ('TEXTCOLOR',(0,0),(-1,0),colors.black),
    ('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 12),
    ('BOTTOMPADDING', (0,0), (-1,0), 5),
    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ], spaceBefore = 15)
    table.setStyle(style)
    rowNumb = length
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.ReportLabLightBlue
        else:
            bc = colors.beige
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        table.setStyle(ts)
        ts = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),1,colors.black),
        #('LINEBEFORE',(2,1),(2,-1),2,colors.red),
        #('LINEABOVE',(0,2),(-1,2),2,colors.green),
        ('GRID',(0,1),(-1,-1),1,colors.black),
        ]
    )
    table.setStyle(ts)
    return table

def getHeading():
    '''return Heading of Scorecard'''
    heading_style = ParagraphStyle(
        name='Heading1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=12,
        textColor=HexColor('#23395d'),
        spaceAfter = 10,
        spaceBefore = 10)
    scorecard_heading = '<b>ScoreCard</b>'
    scorecard_heading = Paragraph(
                        scorecard_heading,
                        heading_style)
    return scorecard_heading

def getDesc(code_base, score, desc_style):
    '''return description of Scorecard'''
    category = ""
    if float(score) <= 2.5:
        category = " (Low Risk)"
    elif float(score) <= 5:
        category = " (Medium Risk)"
    elif float(score) <= 7.5:
        category = " (High Risk)"
    elif float(score) <= 10:
        category = " (Critical Risk)"
    code_base = "Code Base: " + code_base
    risk_score = '<br />' + "Risk Score: <b>"\
                + str(score) +'</b>'\
                + category +'<br />'
    desc = code_base + risk_score \
            + 'Detailed Checks:' + '<br />'
    desc = Paragraph(desc, desc_style)
    return desc

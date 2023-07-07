import json
import requests
import sys
from rich import print
from reportlab.platypus import Paragraph, Table
from reportlab.lib.pagesizes import mm
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from bes_dev_kit.src.risk_summary.New_line_char import insert_newline_char

def fossology(ossp_name, version):
    resp = getApiData(ossp_name, version)
    data = []
    data.append(["File Name",
                 "License Concluded",
                 "File Copyright Text"])
    for obj in resp[1:]:
        sublist = []
        if 'FileName' not in obj or obj["FileName"] == "":
            continue
        file_name = insert_newline_char(obj["FileName"], 26, '/')
        sublist.append(file_name)
        sublist.append(insert_newline_char(obj["LicenseConcluded"], 20, ' '))
        file_copyright_text = insert_newline_char(obj["FileCopyrightText"], 37, ' ')
        sublist.append(file_copyright_text)
        data.append(sublist)

    desc_style = ParagraphStyle(
        name='descStyle',
        leading=12,
        fontSize=11,
        spaceAfter = 10,
        spaceBefore = 10
    )
    fossology_heading = getHeading()
    desc = getDesc(ossp_name, version, desc_style)
    table = getTable(data)
    tool_desc = getToolDesc(desc_style)
    pages = [
        fossology_heading,
        desc,
        table,
        tool_desc
    ]
    return pages

def getApiData(ossp_name, version):
    try:
        url = 'https://raw.githubusercontent.com/Be-Secure/'\
            'besecure-assessment-datastore/main/'\
            + ossp_name + '/' + version + \
            '/license-compliance/'\
            + ossp_name + '-' + version + \
            '-fossology-report.json'
        resp = requests.get(url, timeout=5)
        # verify=False,
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
        print(f'[bold red]Alert! Invalid input or Fossology'+
              ' report not available for',ossp_name)
        sys.exit(1)
    return json.loads(resp.text)

def getTable(data):
    table = Table(data, colWidths=(55*mm, 50*mm, 80*mm), repeatRows=1)
    style = TableStyle([
    ('BACKGROUND', (0,0), (3,0), colors.ReportLabBlueOLD),
    ('TEXTCOLOR',(0,0),(-1,0),colors.black),
    ('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 12),
    ('BOTTOMPADDING', (0,0), (-1,0), 5),
    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ])
    table.setStyle(style)
    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.ReportLabLightBlue
        else:
            bc = colors.beige
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        table.setStyle(ts)
    # 3) Add borders
    ts = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),1,colors.black),
        ('GRID',(0,1),(-1,-1),1,colors.black),
        ]
    )
    table.setStyle(ts)
    return table

def getHeading():
    heading_style = ParagraphStyle(
        name='Heading1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=12,
        textColor=HexColor('#23395d'),
        spaceAfter = 10,
        spaceBefore = 15
    )
    fossology_heading = '<b>License Compliance Review</b>'
    fossology_heading = Paragraph(fossology_heading, heading_style)
    return fossology_heading

def getDesc(ossp_name, version, desc_style):
    desc = 'License compliance check '\
        'is a simple text scan through '\
        'the entire code base to '\
        'detect any kind of license file '\
        'or copyright text exists in the '\
        'code base. This will help us review '\
        'whether the codebase has any license '\
        'or copyright text that is incompatible '\
        'with '+ossp_name+'(Version: '+version+')'\
        ' license. The table shows the output'\
        ' from the Fossology tool and the license'\
        ' and copyright text are very minimal. '\
        'The action item here is to figure out '\
        'whether this is relevant and clean up '\
        'the code if it not required.'
    desc = Paragraph(desc, desc_style)
    return desc

def getToolDesc(desc_style):
    tool_desc = '<b>Tool: Fossology</b> is an '\
        'open-source license compliance software '\
        'system and toolkit. As a toolkit, '\
        'fossology provides the functionality '\
        'to run license, copyright, and export '\
        'control scans from the command line. As '\
        'a system, it provides a database and '\
        'web UI to give a compliance workflow. '\
        'License, copyright, and export scanners '\
        'are tools available for compliance activities.'
    tool_desc = Paragraph(tool_desc, desc_style)
    return tool_desc

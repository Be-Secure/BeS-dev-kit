import sys
import json, requests
from reportlab.platypus import Paragraph, Table
from reportlab.lib.pagesizes import mm
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from rich import print
from bes_dev_kit.src.risk_summary.New_line_char import insert_newline_char

def sbom(OSSP_Name, version):
    '''return pdf elements of SBOM'''
    try:
        url = 'https://raw.githubusercontent.com/Be-Secure/'\
            'besecure-assessment-datastore/main/'\
            +OSSP_Name+'/'+version+\
            '/sbom/'\
            +OSSP_Name+'-'+version+\
            '-sbom-report.json'
        resp = requests.get(url, timeout=5)
    except requests.exceptions.HTTPError:
        print("HTTP Error")
        sys.exit(1)
    except requests.exceptions.ReadTimeout:
        print("Request time out")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Connection error")
        sys.exit(1)
    except requests.exceptions.RequestException:
        print("Exception request")
        sys.exit(1)
    if resp.text == '404: Not Found':
        print(f'[bold red]Alert! [green]Invalid '+
              'input or SBOM'+
              ' report not available fo', OSSP_Name)
        sys.exit(1)
    resp = json.loads(resp.text)
    data = []
    data.append(["Name","Version Info","Supplier"])
    for obj in resp["packages"]:
        if 'name' not in obj:
            continue
        sublist = []
        name = insert_newline_char(obj["name"],25, '-')
        sublist.append(name)
        if 'versionInfo' in obj:
            sublist.append(
                insert_newline_char(obj["versionInfo"],
                13,
                ' ')
            )
        else:
            sublist.append("Not Available")
        supplier = insert_newline_char(obj["supplier"], 55, ' ')
        sublist.append(supplier)
        data.append(sublist)
    creator = resp["creationInfo"]["creators"]
    tool = "<b>" + creator[len(creator)-1] + "</b>"
    table = Table(data, colWidths=(50*mm, 35*mm, 100*mm), repeatRows=1)
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
        #('LINEBEFORE',(2,1),(2,-1),2,colors.red),
        #('LINEABOVE',(0,2),(-1,2),2,colors.green),
        ('GRID',(0,1),(-1,-1),1,colors.black),
        ]
    )
    table.setStyle(ts)
    heading_style = ParagraphStyle(
        name='Heading1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=12,
        textColor=HexColor('#23395d'),
        spaceAfter = 10,
        spaceBefore = 15)
    sbom_heading = '<b>Dependency Review Using '\
        'Software Bill of Materials (SBOM)</b>'
    sbom_heading = Paragraph(sbom_heading, heading_style)
    desc = 'A “software bill of materials” '\
        '(SBOM) has emerged as a key building'\
        ' block in software supply chain risk '\
        'management. It is a complete, formally'\
        ' structured list of components, libraries,'\
        ' and modules that are required to build'\
        ' (i.e., compile and link) a given piece '\
        'of software and the supply chain relationships'\
        ' between them. An SBOM is useful to producers'\
        ' and consumers of software, as it provides'\
        ' software transparency, software integrity,'\
        ' and software identity benefits.'
    desc_style = ParagraphStyle(
        name='descStyle',
        leading=12,
        fontSize=11,
        spaceAfter = 10,
        spaceBefore = 10)
    desc = Paragraph(desc, desc_style)
    tool = Paragraph(tool, desc_style)
    elems = [
        sbom_heading,
        desc,
        table,
        tool
    ]
    return elems
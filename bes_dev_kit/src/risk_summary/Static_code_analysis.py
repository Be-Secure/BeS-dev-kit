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

def sonarqube(OSSP_Name, version):
    '''return pdf elements of sonarqube'''
    try:
        url = 'https://raw.githubusercontent.com/'\
            'Be-Secure/'\
            'besecure-assessment-datastore/main/'\
            +OSSP_Name+'/'+version+\
            '/sast/'\
            +OSSP_Name+'-'+version+\
            '-sonarqube-report.json'
        resp = requests.get(url, timeout=5)
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
        print(f'[bold red]Alert! [green]Invalid '+
              'input or Sonarqube'+
              ' report not available for', OSSP_Name)
        sys.exit(1)
    resp = json.loads(resp.text)
    data = []
    data.append(["Issue Type",
                 "Percentage/\nNo. of issues",
                 "Description"])
    duplication_desc = "For Java projects there "\
        "should be at least 10 successive and "\
        "duplicated statements whatever the "\
        "number of tokens and lines. Differences "\
        "in indentation and in string literals are "\
        "ignored while detecting duplications."
    duplication_desc = insert_newline_char(
                        duplication_desc,
                        53, ' ')
    bug_desc = "A coding mistake that can "\
        "lead to an error or unexpected "\
        "behaviour at runtime"
    bug_desc = insert_newline_char(bug_desc, 55, ' ')
    vulnerability_desc = "A point in your code "\
        "that's open to cyber-attack"
    vulnerability_desc = insert_newline_char(
                        vulnerability_desc,
                        55, ' ')
    code_smell_desc = "A maintainability issue that "\
        "makes your code confusing and "\
        "diffucult to maintain"
    code_smell_desc = insert_newline_char(
                    code_smell_desc,
                    55, ' ')
    issues = resp['issues']
    duplication_count = 0
    code_smell_count = 0
    bug_count = 0
    vulnerability_count = 0
    major = 0
    minor = 0
    critical = 0
    info = 0 
    blocker = 0
    duplication_list=[
        'Duplication',
        'Duplication.'
    ]
    for issue in issues:
        if isinstance(issue, dict) and 'flows' in issue and issue['flows']:
            for flow in issue['flows']:
                for location in flow['locations']:
                    if location.get('msg') in duplication_list:
                        duplication_count += 1
        if 'type' in issue:
            if issue['type'] == "CODE_SMELL":
                code_smell_count += 1
                if issue['severity'] == 'MAJOR':
                    major += 1
                elif issue['severity'] == 'CRITICAL':
                    critical += 1
                elif issue['severity'] == 'MINOR':
                    minor += 1
                elif issue['severity'] == 'INFO':
                    info += 1
                elif issue['severity'] == 'BLOCKER':
                    blocker += 1
            elif issue['type'] == "BUG":
                bug_count += 1
            elif issue['type'] == "VULNERABILITY":
                vulnerability_count += 1

    data.append([
        "Duplications",
        duplication_count,
        duplication_desc
    ])
    data.append([
        "Bugs",
        bug_count,
        bug_desc
    ])
    data.append([   
        "Vulnerability",
        vulnerability_count,
        vulnerability_desc
    ])

    code_smell_count = "Total: " + str(code_smell_count)
    if blocker > 0:
        blocker = "\nBlocker: " + str(blocker)
        code_smell_count += blocker
    if critical > 0:
        critical = "\nCritical: " + str(critical)
        code_smell_count += critical
    if major > 0:
        major = "\nMajor: " + str(major)
        code_smell_count += major
    if minor > 0:
        minor = "\nMinor: " + str(minor)
        code_smell_count += minor
    if info > 0:
        info = "\nInfo: " + str(info)
        code_smell_count += info
    data.append([
        "Code Smells",
        code_smell_count,
        code_smell_desc
    ])
    table = Table(data, colWidths=(35*mm, 50*mm, 100*mm), repeatRows=1)
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

    ts = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),1,colors.black),
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
        spaceBefore = 10)
    sonarqube_heading = '<b>Static Code Analysis</b>'
    sonarqube_heading = Paragraph(
                        sonarqube_heading,
                        heading_style)
    desc = 'Codebase: github.com/Be-Secure/' + OSSP_Name
    tool_desc = '<b>Tool: Sonarqube</b> is an '\
        'open-source platform for continuous '\
        'inspection of code quality to perform'\
        ' automatic reviews with static analysis'\
        ' of code to detect bugs and code smells'\
        ' on 30+ programming languages. SonarQube '\
        'offers reports on duplicated code, coding '\
        'standards, unit tests, code coverage, code '\
        'complexity, comments, bugs, and security'\
        ' recommendations. In SonarQube a Quality'\
        ' Gate is a set of conditions the project '\
        'must meet before it can qualify for '\
        'production release.'
    desc_style = ParagraphStyle(
        name='descStyle',
        leading=12,
        fontSize=11,
        spaceAfter = 10,
        spaceBefore = 10)
    desc = Paragraph(desc, desc_style)
    tool_desc = Paragraph(tool_desc, desc_style)
    elems = [
        sonarqube_heading,
        desc,
        table,
        tool_desc
    ]
    return elems
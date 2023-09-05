from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from PyPDF2 import PdfMerger
import os


def count(number :[int]) -> int:
    sum = 0
    for i in number:
        if i != 0:
            sum += 1
    return sum



def txtProcessor(txt_file):
    names = {}
    
    try:
        with open(txt_file, "r") as f:
            data = f.read()
            data = data.split("\n")
            data = [x.split(",") for x in data]
            
            for item in data:
                   
                if item[0].startswith('%^$@#'):
                    new_name = ' '.join(item[0].split()[1:3])
                    new_name = new_name.split()[0].split('!')[0]+ " " + new_name.split()[1] + "\nTotal hours: "
                    value = int(item[0].split()[-1])
                    if new_name not in names:
                        names[new_name] = []
                    names[new_name].append(value)
                    
                if item[0].startswith('H4URS'):
                    hours = item[0].split()[-1]
            n = max([len(v) for v in names.values()])
            table = [[x for x in range(0, n + 1)]] + [[k] + v for k, v in names.items()]
            for employee in table[1:]:
                employee[0] = employee[0].replace("\nTotal hours: ", "\nTotal hours: " + str(count(employee[1:])*8))
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return table, hours

def merge_pdfs(files :[str], output: str):
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    merger.write(output)
    merger.close()

def deleteFiles(files :[str]):
    for file in files:
        os.remove(file)


def generatePDF(number :int, maxNumber :int):
    # Create a PDF document
    pdf_file = "work_schedule"+str(number)+".pdf"
    document = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))

    # Create a list to hold the data for the table
    data, hours = txtProcessor("output.txt")

    # Create a table and set its style
    table = Table(data)

    # Style the table
    style = TableStyle([
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    for row_num in range(1,len(data)):
        for col_num in range(1,len(data[row_num])):
            cell_data = data[row_num][col_num]
            if cell_data == 0:
                style.add('BACKGROUND', (col_num,row_num),(col_num,row_num),colors.whitesmoke)
                style.add('TEXTCOLOR', (col_num,row_num),(col_num,row_num),colors.whitesmoke)
            elif cell_data == 1:
                style.add('BACKGROUND', (col_num,row_num),(col_num,row_num),colors.lightblue)
            elif cell_data == 2:
                style.add('BACKGROUND', (col_num,row_num),(col_num,row_num),colors.blue)
            elif cell_data == 3:
                style.add('BACKGROUND', (col_num,row_num),(col_num,row_num),colors.darkblue)

    table.setStyle(style)

    # Get the sample style sheet
    styles = getSampleStyleSheet()

    # Create a title paragraph using the Heading1 style
    title = Paragraph("Total hours: " + str(hours) + "\n Schedule no." + str(number), styles["Heading1"])

    # Build the PDF document
    elements = [title, table]
    document.build(elements)

    print(f"Schedule {number} generated")

    if number == maxNumber-1:
        print("Merging schedules...")
        merge_pdfs([f"work_schedule{x}.pdf" for x in range(0, number+1)], "work_schedule.pdf")
        print("schedules merged")
        print("Deleting schedules...")
        deleteFiles([f"work_schedule{x}.pdf" for x in range(0, number+1)])

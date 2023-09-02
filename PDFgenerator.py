from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



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
                    value = int(item[0].split()[-1])
                    if new_name not in names:
                        names[new_name] = []
                    names[new_name].append(value)

            n = max([len(v) for v in names.values()])
            table = [[x for x in range(0, n + 1)]] + [[k] + v for k, v in names.items()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return table

def generatePDF():
    # Create a PDF document
    pdf_file = "work_schedule.pdf"
    document = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))

    # Create a list to hold the data for the table
    data = txtProcessor("output.txt")

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

    # Build the PDF document
    elements = [table]
    document.build(elements)

    print(f"PDF generated: {pdf_file}")

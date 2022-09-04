def write_one_line_into_pdf(pdf, string, align):
    if not string:
        string = ""
    if type(string) == list:
        string = str(string)
    pdf.cell(200, 10, txt=str(string), ln=1, align=align)

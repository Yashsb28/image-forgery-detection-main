from fpdf import FPDF

pdf = FPDF ('P','mm','Letter')

pdf.add_page()

pdf.set_font('helvetica','',16)

pdf.cell(100,10,'Image Forgery Detection', border=True)
pdf.ln()

pdf.output('pdf_1.pdf') 
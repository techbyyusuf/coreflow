import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('Vera-Bold', 'VeraBd.ttf'))


def impressum(my_canvas, width):
    my_canvas.setFont('Vera', 10)
    name = "Max Mustermann"
    street = "Musterstraße, 89"
    city = "D-80000 Musterstadt"
    my_canvas.drawRightString(width-40, 700, name)
    my_canvas.drawRightString(width-40, 687, street)
    my_canvas.drawRightString(width-40, 674, city)
    # my_canvas.drawString(420, 670,"Tel. +49 777 000-0")
    # my_canvas.drawString(420, 660,"Fax. +49 777 000-1")
    # my_canvas.drawString(420, 650,"E-Mail: info@muster.de")


def customer_details(my_canvas, company_name, customer_name, customer_street, customer_city):
    my_canvas.setFont('Vera', 10)
    my_canvas.drawString(x=40, y= 720, text=company_name)
    my_canvas.drawString(x=40, y=707, text=customer_name)
    my_canvas.drawString(x=40, y=694, text=customer_street)
    my_canvas.drawString(x=40, y=681, text=customer_city)


def impressum_small(my_canvas):
    my_canvas.setFont('Vera', 7)
    my_canvas.drawString(x=40, y=80, text="Max Mustermann")
    my_canvas.drawString(x=40, y=72, text="Musterstraße, 89")
    my_canvas.drawString(x=40, y=64, text="D-80000 Musterstadt")
    my_canvas.drawString(x=40, y=56, text="Tel. +49 777 000-0")
    my_canvas.drawString(x=40, y=48, text="Fax. +49 777 000-1")
    my_canvas.drawString(x=40, y=40, text="E-Mail: info@muster.de")


def bank_details(my_canvas):
    my_canvas.setFont('Vera', 7)
    my_canvas.drawString(x=230, y=80, text="Kreditinstitut: Commerzbank")
    my_canvas.drawString(x=230, y=72, text="IBAN: DE3423 4562 3435 6765")
    my_canvas.drawString(x=230, y=64, text="BIC: COBADEFFXXX")
    my_canvas.drawString(x=230, y=56, text="Kto. Inh.: Max Mustermann")


def tax_details(my_canvas, width):
    my_canvas.setFont('Vera', 7)
    my_canvas.drawRightString(x=width-40, y=80, text="USt-ID: DE24324567")
    my_canvas.drawRightString(x=width-40, y=72, text="HRB: 12345678")
    my_canvas.drawRightString(x=width-40, y=64, text="Amtsgericht: Charlottenburg")
    my_canvas.drawRightString(x=width-40, y=56, text="Geschäftsführer: Max Mustermann")
    my_canvas.drawRightString(x=width-40, y=48, text="Webseite: www.firma.de")


def title(my_canvas):
    my_canvas.setFont(psfontname='Vera-Bold', size=18)
    my_canvas.drawString(x=40, y=560, text="Rechnung")


def first_notice(my_canvas):
    my_canvas.setFont('Vera', 10)
    my_canvas.drawString(
        x=40,
        y=520,
        text=f"Sehr geehrte Damen und Herren"
    )
    my_canvas.drawString(
        x=40,
        y=492,
        text="vielen Dank, für Ihren Auftrag. Vereinbarungsgemäß berechnen wir "
             "ihnen hiermit folgende"
    )
    my_canvas.drawString(x=40, y=479, text="Leistungen:")


def last_notice(my_canvas):
    my_canvas.setFont('Vera', 10)

    my_canvas.drawString(
        x=40,
        y=226,
        text="Bitte überweisen Sie den Rechnungsbetrag innerhalb von 14 Tagen auf unser unten genanntes"
    )
    my_canvas.drawString(x=40, y=213, text="Konto.")
    my_canvas.drawString(x=40, y=200,
                         text="Für weitere Fragen stehen wir ihnen gerne zu Verfügung.")
    my_canvas.drawString(x=40, y=163, text="Mit freundlichen Grüßen")
    my_canvas.drawString(x=40, y=150, text="Max Mustermann")


def date_and_invoice_number(invoice, my_canvas, width):
    my_canvas.setFont('Vera', 10)

    invoice_date = "Datum: " + date.today().strftime('%d.%m.%Y')
    my_canvas.drawRightString(x=width-40 , y=651, text=invoice_date)

    invoice_number_in_str = "Rechnungsnummer: " + str(invoice.invoice_number)
    my_canvas.drawRightString(x=width-40, y=638, text=invoice_number_in_str)


def generate_pdf(invoice, company_name, name, street, city):
    file_path = f"{invoice.invoice_number}.pdf"
    my_canvas = canvas.Canvas(filename=file_path, pagesize=A4)
    width, height = A4

    my_canvas.drawImage("assets/logo.png", x=30, y=height - 70, width=110, height=35)
    impressum(my_canvas, width)
    date_and_invoice_number(my_canvas=my_canvas, invoice=invoice, width=width)
    customer_details(my_canvas, company_name, name, street, city)
    title(my_canvas)
    first_notice(my_canvas)
    impressum_small(my_canvas)
    bank_details(my_canvas)
    tax_details(my_canvas, width)
    last_notice(my_canvas)

    my_canvas.showPage()
    my_canvas.save()
    return file_path

#os.startfile("invoice.pdf")

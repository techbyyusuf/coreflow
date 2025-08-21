import os
import re
from pathlib import Path
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

PDF_DIR = Path(os.getenv("PDF_DIR", "generated_pdfs")).resolve()
ASSETS_DIR = Path(os.getenv("ASSETS_DIR", "assets")).resolve()
LOGO_PATH = Path(os.getenv("LOGO_PATH", ASSETS_DIR / "logo.png")).resolve()
FONTS_DIR = Path(os.getenv("FONTS_DIR", ASSETS_DIR / "fonts")).resolve()
FONT_REGULAR = FONTS_DIR / "Vera.ttf"
FONT_BOLD_TTF = FONTS_DIR / "VeraBd.ttf"
LEFT, RIGHT, BOTTOM, TOP = 40, 40, 40, 40

if FONT_REGULAR.exists():
    pdfmetrics.registerFont(TTFont("Vera", str(FONT_REGULAR)))
if FONT_BOLD_TTF.exists():
    pdfmetrics.registerFont(TTFont("VeraBd", str(FONT_BOLD_TTF)))
registerFontFamily(
    "Vera",
    normal="Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica",
    bold="VeraBd" if "VeraBd" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold",
    italic="Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica",
    boldItalic="VeraBd" if "VeraBd" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold",
)

PDF_DIR.mkdir(parents=True, exist_ok=True)

from pdf_service.table_for_invoice import draw_items_table_and_totals, make_pdf_items_from_invoice

def _draw_right(c, width, y, text, offset=RIGHT):
    c.drawRightString(x=width - offset, y=y, text=str(text))

def _safe_filename(invoice_number):
    name = re.sub(r"[^A-Za-z0-9._-]", "_", f"{invoice_number}")
    return name if name.endswith(".pdf") else f"{name}.pdf"

def impressum(c, width):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 10)
    _draw_right(c, width, 700, "Max Mustermann")
    _draw_right(c, width, 687, "Musterstraße 89")
    _draw_right(c, width, 674, "D-80000 Musterstadt")

def customer_details(c, company_name, customer_name, street, city):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 10)
    c.drawString(LEFT, 720, company_name)
    c.drawString(LEFT, 707, customer_name)
    c.drawString(LEFT, 694, street)
    c.drawString(LEFT, 681, city)

def impressum_small(c):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 7)
    c.drawString(LEFT, 80, "Max Mustermann")
    c.drawString(LEFT, 72, "Musterstraße 89")
    c.drawString(LEFT, 64, "D-80000 Musterstadt")
    c.drawString(LEFT, 56, "Tel. +49 777 000-0")
    c.drawString(LEFT, 48, "Fax +49 777 000-1")
    c.drawString(LEFT, 40, "E-Mail: info@muster.de")

def bank_details(c):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 7)
    c.drawString(230, 80, "Kreditinstitut: Commerzbank")
    c.drawString(230, 72, "IBAN: DE34 2345 6234 3567 65")
    c.drawString(230, 64, "BIC: COBADEFFXXX")
    c.drawString(230, 56, "Kontoinhaber: Max Mustermann")

def tax_details(c, width):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 7)
    _draw_right(c, width, 80, "USt-ID: DE24324567")
    _draw_right(c, width, 72, "HRB: 12345678")
    _draw_right(c, width, 64, "Amtsgericht: Charlottenburg")
    _draw_right(c, width, 56, "Geschäftsführer: Max Mustermann")
    _draw_right(c, width, 48, "Webseite: www.firma.de")

def title(c):
    c.setFont("VeraBd" if "VeraBd" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold", 18)
    c.drawString(LEFT, 560, "Rechnung")

def first_notice(c):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 10)
    c.drawString(LEFT, 520, "Sehr geehrte Damen und Herren,")
    c.drawString(LEFT, 492, "vielen Dank für Ihren Auftrag. Vereinbarungsgemäß berechnen wir Ihnen hiermit folgende Leistungen:")

def last_notice(c):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 10)
    c.drawString(LEFT, 226, "Bitte überweisen Sie den Rechnungsbetrag innerhalb von 14 Tagen auf unser unten genanntes Konto.")
    c.drawString(LEFT, 200, "Für weitere Fragen stehen wir Ihnen gerne zur Verfügung.")
    c.drawString(LEFT, 176, "Mit freundlichen Grüßen")
    c.drawString(LEFT, 163, "Max Mustermann")

def date_and_invoice_number(invoice, c, width):
    c.setFont("Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 10)
    _draw_right(c, width, 651, "Datum: " + date.today().strftime("%d.%m.%Y"))
    _draw_right(c, width, 638, f"Rechnungsnummer: {invoice.invoice_number}")

def generate_pdf(invoice, company_name, name, street, city):
    safe_name = _safe_filename(invoice.invoice_number)
    out_path = (PDF_DIR / safe_name).resolve()
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    c = canvas.Canvas(filename=str(tmp_path), pagesize=A4)
    width, height = A4
    c.setAuthor("Max Mustermann")
    c.setTitle(f"Rechnung {invoice.invoice_number}")
    if LOGO_PATH.exists():
        c.drawImage(str(LOGO_PATH), x=30, y=height - 70, width=110, height=35, preserveAspectRatio=True, mask="auto")
    impressum(c, width)
    date_and_invoice_number(invoice, c, width)
    customer_details(c, company_name, name, street, city)
    title(c)
    first_notice(c)
    items = make_pdf_items_from_invoice(invoice)
    draw_items_table_and_totals(c, items, y_top=470, y_bottom=230)
    impressum_small(c)
    bank_details(c)
    tax_details(c, width)
    last_notice(c)
    c.save()
    os.replace(tmp_path, out_path)
    return out_path

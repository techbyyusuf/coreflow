from decimal import Decimal
from reportlab.platypus import Table, LongTable, TableStyle, Paragraph, Frame, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics

LEFT, RIGHT, TOP, BOTTOM = 40, 40, 40, 40
FONT_BODY = "Vera" if "Vera" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
FONT_BOLD = "VeraBd" if "VeraBd" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"

STYLE_BODY = ParagraphStyle(name="Body", fontName=FONT_BODY, fontSize=10, leading=12, alignment=0)
STYLE_HEADER = ParagraphStyle(name="Header", fontName=FONT_BOLD, fontSize=10, leading=12, alignment=0)
STYLE_NUM = ParagraphStyle(name="Num", fontName=FONT_BODY, fontSize=10, leading=12, alignment=2)

def _eur(x):
    v = Decimal(x)
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} €"

def draw_items_table_and_totals(c, items, y_top=470, y_bottom=230, vat_rate=Decimal("0.19")):
    page_w, page_h = A4
    usable_w = page_w - LEFT - RIGHT
    w_pos, w_qty, w_unit, w_unit_price, w_total = 40, 45, 55, 80, 90
    w_desc = usable_w - (w_pos + w_qty + w_unit + w_unit_price + w_total)
    col_widths = [w_pos, w_qty, w_unit, w_desc, w_unit_price, w_total]
    header = [
        Paragraph("Position", STYLE_HEADER),
        Paragraph("Anzahl", STYLE_HEADER),
        Paragraph("Einheit", STYLE_HEADER),
        Paragraph("Bezeichnung", STYLE_HEADER),
        Paragraph("Einzelpreis", STYLE_HEADER),
        Paragraph("Gesamtpreis", STYLE_HEADER),
    ]
    data = [header]
    subtotal = Decimal("0.00")
    for idx, it in enumerate(items, start=1):
        pos = it.get("position", idx)
        qty = Decimal(str(it["qty"]))
        unit = it.get("unit", "")
        desc = it.get("description", "")
        unit_price = Decimal(str(it["unit_price_net"]))
        line_total = (qty * unit_price).quantize(Decimal("0.01"))
        subtotal += line_total
        data.append([
            Paragraph(str(pos), STYLE_BODY),
            Paragraph(f"{qty.normalize()}", STYLE_NUM),
            Paragraph(unit, STYLE_BODY),
            Paragraph(desc, STYLE_BODY),
            Paragraph(_eur(unit_price), STYLE_NUM),
            Paragraph(_eur(line_total), STYLE_NUM),
        ])
    items_table = LongTable(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    items_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E5E5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("ALIGN", (4, 1), (5, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (4, 1), (5, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#BBBBBB")),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor("#BBBBBB")),
    ]))
    vat_amount = (subtotal * vat_rate).quantize(Decimal("0.01"))
    total_gross = subtotal + vat_amount
    sums_data = [
        [Paragraph("Nettopreis", STYLE_BODY), Paragraph(_eur(subtotal), STYLE_NUM)],
        [Paragraph(f"Zzgl. {int(vat_rate*100)}% USt.", STYLE_BODY), Paragraph(_eur(vat_amount), STYLE_NUM)],
        [Paragraph("Rechnungsbetrag", STYLE_HEADER), Paragraph(_eur(total_gross), STYLE_NUM)],
    ]
    w_amount = 140
    sums_table = Table(sums_data, colWidths=[usable_w - w_amount, w_amount], hAlign="RIGHT")
    sums_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("RIGHTPADDING", (1, 0), (1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E5E5E5")),
        ("FONTNAME", (0, -1), (-1, -1), FONT_BOLD),
        ("BOX", (0, -1), (-1, -1), 0.25, colors.HexColor("#BBBBBB")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story = [items_table, Spacer(1, 18), sums_table]
    first_frame = Frame(x1=LEFT, y1=y_bottom, width=usable_w, height=(y_top - y_bottom), leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    first_frame.addFromList(story, c)
    while story:
        c.showPage()
        next_frame = Frame(x1=LEFT, y1=BOTTOM, width=usable_w, height=(page_h - TOP - BOTTOM), leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        next_frame.addFromList(story, c)

def make_pdf_items_from_invoice(invoice):
    pdf_items = []
    for idx, it in enumerate(invoice.items, start=1):
        prod = it.product
        pdf_items.append({
            "position": idx,
            "qty": Decimal(str(it.quantity)),
            "unit": (getattr(prod, "unit", None) or "Stück"),
            "description": getattr(prod, "name", "") or getattr(prod, "description", ""),
            "unit_price_net": Decimal(str(it.unit_price)),
        })
    return pdf_items

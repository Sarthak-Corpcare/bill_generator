from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime
from decimal import Decimal
from io import BytesIO        # ✅ import BytesIO for in-memory buffer
import streamlit as st


def money(val):
    return f"Rs {Decimal(val):.2f}"


def generate_bill_pdf():
    """Generate a restaurant bill and return PDF bytes."""
    buffer = BytesIO()  # ✅ create in-memory buffer

    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    left_margin = 20 * mm
    right_margin = width - 20 * mm
    y = height - 25 * mm

    # --- Restaurant Info ---
    restaurant = {
        "name": "The Spicy Spoon",
        "address": "123 Curry Lane, Foodie City, 400001",
        "phone": "+91 98765 43210",
        "gstin": "27ABCDE1234F1Z5",
    }

    bill = {
        "bill_no": "BILL-1023",
        "table": "T5",
        "date": datetime.now(),
        "items": [
            {"name": "Paneer Butter Masala", "qty": 2, "rate": 410.00},
            {"name": "Garlic Naan", "qty": 4, "rate": 80.00},
            {"name": "Jeera Rice", "qty": 1, "rate": 180.00},
            {"name": "Gulab Jamun (2 pcs)", "qty": 1, "rate": 80.00},
        ],
        "gst_percent": 5.0,
    }

    footer_text = "Thank you! Please visit again.\nThis is a computer-generated bill."

    # --- Header ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, restaurant["name"])
    y -= 7 * mm
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, y, restaurant["address"])
    y -= 4 * mm
    c.drawCentredString(width / 2, y, f"Phone: {restaurant['phone']} | GSTIN: {restaurant['gstin']}")
    y -= 8 * mm

    # --- Bill Info ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_margin, y, f"Bill No: {bill['bill_no']}")
    c.drawRightString(right_margin, y, f"Date: {bill['date'].strftime('%d-%b-%Y %I:%M %p')}")
    y -= 5 * mm
    c.setFont("Helvetica", 9)
    c.drawString(left_margin, y, f"Table: {bill['table']}")
    y -= 8 * mm

    # --- Column Layout ---
    col_item_x = left_margin
    col_qty_x = right_margin - 130
    col_rate_x = right_margin - 70
    col_amt_x = right_margin

    # --- Table Header ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col_item_x, y, "Item")
    c.drawRightString(col_qty_x, y, "Qty")
    c.drawRightString(col_rate_x, y, "Rate")
    c.drawRightString(col_amt_x, y, "Amount")
    y -= 5 * mm
    c.line(left_margin, y, right_margin, y)
    y -= 4 * mm

    # --- Items ---
    c.setFont("Helvetica", 9)
    subtotal = 0
    for item in bill["items"]:
        name = item["name"]
        qty = item["qty"]
        rate = item["rate"]
        amount = qty * rate
        subtotal += amount

        c.drawString(col_item_x, y, name)
        c.drawRightString(col_qty_x, y, str(qty))
        c.drawRightString(col_rate_x, y, money(rate))
        c.drawRightString(col_amt_x, y, money(amount))
        y -= 7 * mm

    # --- Totals ---
    c.line(left_margin, y, right_margin, y)
    y -= 6 * mm

    gst = subtotal * bill["gst_percent"] / 100
    grand_total = subtotal + gst

    c.setFont("Helvetica", 9)
    c.drawRightString(col_rate_x, y, "Subtotal:")
    c.drawRightString(col_amt_x, y, money(subtotal))
    y -= 6 * mm

    c.drawRightString(col_rate_x, y, f"GST @{bill['gst_percent']}%:")
    c.drawRightString(col_amt_x, y, money(gst))
    y -= 8 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(col_rate_x, y, "Grand Total:")
    c.drawRightString(col_amt_x, y, money(grand_total))
    y -= 12 * mm

    # --- Footer ---
    c.setFont("Helvetica", 8)
    for line in footer_text.splitlines():
        c.drawCentredString(width / 2, y, line)
        y -= 4 * mm

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


# --- Streamlit UI ---
st.set_page_config(page_title="Restaurant Bill Generator", page_icon="🧾")
st.title("🍽️ Restaurant Bill PDF Generator")
st.write("Click below to download your generated bill as a PDF.")

pdf_bytes = generate_bill_pdf()

st.download_button(
    label="📥 Download Bill PDF",
    data=pdf_bytes,
    file_name="restaurant_bill.pdf",
    mime="application/pdf"
)

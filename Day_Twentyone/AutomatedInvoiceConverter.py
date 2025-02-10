from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import messagebox, simpledialog


def generate_invoice(invoice_data, filename="invoice.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, height - 50, "Invoice")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100,
                 f"Invoice Number: {invoice_data['invoice_number']}")
    c.drawString(50, height - 120,
                 f"Customer Name: {invoice_data['customer_name']}")
    c.drawString(50, height - 140, f"Date: {invoice_data['date']}")

    y_position = height - 180
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Item")
    c.drawString(250, y_position, "Quantity")
    c.drawString(350, y_position, "Price")
    c.drawString(450, y_position, "Total")
    c.line(50, y_position - 10, 550, y_position - 10)

    y_position -= 30
    total_amount = 0
    c.setFont("Helvetica", 12)
    for item in invoice_data['items']:
        c.drawString(50, y_position, item['name'])
        c.drawString(250, y_position, str(item['quantity']))
        c.drawString(350, y_position, f"${item['price']:.2f}")
        item_total = item['quantity'] * item['price']
        c.drawString(450, y_position, f"${item_total:.2f}")
        total_amount += item_total
        y_position -= 20

    c.line(50, y_position - 10, 550, y_position - 10)
    y_position -= 30
    c.drawString(350, y_position, "Total Amount:")
    c.drawString(450, y_position, f"${total_amount:.2f}")

    c.save()
    messagebox.showinfo("Success", f"Invoice saved as {filename}")


def get_invoice_data():
    root = tk.Tk()
    root.withdraw()

    invoice_number = simpledialog.askstring("Input", "Enter Invoice Number:")
    customer_name = simpledialog.askstring("Input", "Enter Customer Name:")
    date = simpledialog.askstring("Input", "Enter Date (DD-MM-YYY):")

    items = []
    while True:
        item_name = simpledialog.askstring(
            "Input", "Enter Item Name (or leave blank to finish):")
        if not item_name:
            break
        quantity = simpledialog.askinteger("Input", "Enter Quantity:")
        price = simpledialog.askfloat("Input", "Enter Price:")
        items.append({"name": item_name, "quantity": quantity, "price": price})

    return {"invoice_number": invoice_number, "customer_name": customer_name, "date": date, "items": items}


if __name__ == "__main__":
    invoice_data = get_invoice_data()
    output_filename = f"invoice_{invoice_data['invoice_number']}.pdf"
    generate_invoice(invoice_data, output_filename)

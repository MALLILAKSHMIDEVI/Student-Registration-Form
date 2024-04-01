import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import re
import os
from PyPDF2 import PdfReader

# Initialize list to store submitted data
submitted_data = []


# Define function to load existing data from PDF
def load_existing_data():
    if os.path.exists("Submitted_Data.pdf"):
        with open("Submitted_Data.pdf", "rb") as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                submitted_data.append(page.extract_text())


# Load existing data when the application starts
load_existing_data()


# Data validation functions
def validate_name(name):
    return bool(name.strip())


def validate_aicte_id(aicte_id):
    return bool(re.match(r'^\d{10}$', aicte_id.strip()))


def validate_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()))


def validate_phone(phone):
    return bool(re.match(r'^\d{10}$', phone.strip()))


def validate_college(college):
    return bool(college.strip())


# PDF generation function
def update_pdf():
    # Generate PDF using reportlab library
    filename = "Submitted_Data.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Define table data and style
    table_data = [["Name", "AICTE ID", "Email", "Phone", "College"]]
    for data in submitted_data:
        table_data.append(data.split('\n'))

    # Define table style
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create table
    table = Table(table_data)
    table.setStyle(table_style)

    # Add table to PDF
    doc.build([table])

    messagebox.showinfo("Success", f"PDF updated successfully! Check {filename}.")


# Validation and submission function
def validate_data():
    # Get input values
    name = name_entry.get()
    aicte_id = aicte_id_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    college = college_entry.get()

    # Validate data
    if not validate_name(name):
        messagebox.showerror("Error", "Please enter a valid name.")
        return
    if not validate_aicte_id(aicte_id):
        messagebox.showerror("Error", "Please enter a valid AICTE ID (10 digits).")
        return
    if not validate_email(email):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return
    if not validate_phone(phone):
        messagebox.showerror("Error", "Please enter a valid phone number (10 digits).")
        return
    if not validate_college(college):
        messagebox.showerror("Error", "Please enter a valid college name.")
        return

    # Add current data to the list
    submitted_data.append(f"{name}\n{aicte_id}\n{email}\n{phone}\n{college}")

    # Update PDF
    update_pdf()

    messagebox.showinfo("Success", "Submission successful!")

    # Clear input fields
    name_entry.delete(0, tk.END)
    aicte_id_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    college_entry.delete(0, tk.END)


# Create tkinter window
root = tk.Tk()
root.title("Student Registration Form")
root.geometry("400x300")

# Create frame for input fields
input_frame = ttk.Frame(root, padding="20")
input_frame.pack()

# Create input fields
name_label = ttk.Label(input_frame, text="Name:")
name_label.grid(row=0, column=0, sticky="w")
name_entry = ttk.Entry(input_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

aicte_id_label = ttk.Label(input_frame, text="AICTE ID:")
aicte_id_label.grid(row=1, column=0, sticky="w")
aicte_id_entry = ttk.Entry(input_frame)
aicte_id_entry.grid(row=1, column=1, padx=5, pady=5)

email_label = ttk.Label(input_frame, text="Email:")
email_label.grid(row=2, column=0, sticky="w")
email_entry = ttk.Entry(input_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

phone_label = ttk.Label(input_frame, text="Phone:")
phone_label.grid(row=3, column=0, sticky="w")
phone_entry = ttk.Entry(input_frame)
phone_entry.grid(row=3, column=1, padx=5, pady=5)

college_label = ttk.Label(input_frame, text="College:")
college_label.grid(row=4, column=0, sticky="w")
college_entry = ttk.Entry(input_frame)
college_entry.grid(row=4, column=1, padx=5, pady=5)

# Create submit button
submit_button = ttk.Button(input_frame, text="Submit", command=validate_data)
submit_button.grid(row=5, columnspan=2, pady=10)

root.mainloop()


import csv
from tkinter import filedialog, messagebox
import sqlite3
from add_function import add_employee
from utils import display_employees

def import_employees(tree):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                add_employee(
                    row['payroll_number'],
                    row['first_name'],
                    row['last_name'],
                    row['work_email'],
                    row['contact_info'],
                    row['department'],
                    row['role'],
                    row['password']
                )
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    messagebox.showerror("Error", f"Employee with payroll number {row['payroll_number']} or email {row['work_email']} already exists!")
                else:
                    messagebox.showerror("Error", "An error occurred while importing the employee. Please try again.")
    display_employees(tree)
    messagebox.showinfo("Success", "Employees imported successfully!")
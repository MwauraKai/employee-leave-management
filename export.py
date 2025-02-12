import csv
from tkinter import filedialog, messagebox
import sqlite3

def export_employees():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with sqlite3.connect("employee_system.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        if not employees:
            messagebox.showinfo("No Data", "No employee data to export.")
            return

        columns = [description[0] for description in cursor.description]

        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(employees)

    messagebox.showinfo("Success", "Employees exported successfully!")
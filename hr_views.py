import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import re
from add_function import add_employee
from authentication import authenticate_user  # Import the authenticate_user function
from delete_function import delete_employee
from update_function import update_employee
from views import view_employees_data
from import_emp import import_employees  # Import the import_employees function
from export import export_employees  # Import the export_employees function
from utils import display_employees  # Import the display_employees function

# Function to fetch HR details based on authenticated user
def get_hr_details(email, password):
    user_details = authenticate_user(email, password)  # Assuming this function returns a dictionary with user details
    if user_details and user_details['role'] == 'HR':
        return user_details
    else:
        messagebox.showerror("Access Denied", "You do not have permission to access the HR dashboard.")
        return None

# Function to search for employees
def search_employees(search_term, department_filter=None, role_filter=None):
    with sqlite3.connect("employee_system.db") as conn:
        cursor = conn.cursor()
        query = '''
            SELECT * FROM employees 
            WHERE (first_name LIKE ? OR last_name LIKE ? OR work_email LIKE ? OR payroll_number LIKE ?)
        '''
        params = ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%')

        if department_filter:
            query += " AND department = ?"
            params += (department_filter,)
        
        if role_filter:
            query += " AND role = ?"
            params += (role_filter,)

        cursor.execute(query, params)
        employees = cursor.fetchall()
    return employees

# Function to show the Add Employee form
def add_employee_form(tree):
    def validate_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def validate_password(password):
        return (len(password) >= 8 and
                re.search(r"[A-Z]", password) and
                re.search(r"[a-z]", password) and
                re.search(r"[0-9]", password) and
                re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    def save_employee():
        payroll_number = payroll_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        work_email = email_entry.get()
        contact_info = contact_entry.get()
        department = department_var.get()
        role = role_var.get()
        password = password_entry.get()

        if not payroll_number or not first_name or not last_name or not work_email or not contact_info or not department or not role or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not validate_email(work_email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not validate_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character.")
            return

        if not contact_info.startswith("+254") or len(contact_info) != 13:
            messagebox.showerror("Error", "Contact info must start with +254 and be 13 characters long.")
            return

        try:
            add_employee(payroll_number, first_name, last_name, work_email, contact_info, department, role, password)
            messagebox.showinfo("Success", "Employee added successfully!")
            add_window.destroy()
            display_employees(tree)  # Update the Treeview dynamically
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", f"Employee with payroll number {payroll_number} or email {work_email} already exists!")
            else:
                messagebox.showerror("Error", "An error occurred while adding the employee. Please try again.")

    add_window = tk.Toplevel()
    add_window.title("Add New Employee")

    tk.Label(add_window, text="Payroll Number").grid(row=0, column=0)
    payroll_entry = tk.Entry(add_window)
    payroll_entry.grid(row=0, column=1)

    tk.Label(add_window, text="First Name").grid(row=1, column=0)
    first_name_entry = tk.Entry(add_window)
    first_name_entry.grid(row=1, column=1)

    tk.Label(add_window, text="Last Name").grid(row=2, column=0)
    last_name_entry = tk.Entry(add_window)
    last_name_entry.grid(row=2, column=1)

    tk.Label(add_window, text="Work Email").grid(row=3, column=0)
    email_entry = tk.Entry(add_window)
    email_entry.grid(row=3, column=1)

    tk.Label(add_window, text="Contact Info").grid(row=4, column=0)
    contact_entry = tk.Entry(add_window)
    contact_entry.grid(row=4, column=1)

    tk.Label(add_window, text="Department").grid(row=5, column=0)
    department_var = tk.StringVar()
    department_menu = tk.OptionMenu(add_window, department_var, "IT", "HR", "Finance", "Legal", "Marketing")
    department_menu.grid(row=5, column=1)

    tk.Label(add_window, text="Role").grid(row=6, column=0)
    role_var = tk.StringVar()
    role_menu = tk.OptionMenu(add_window, role_var, "Employee", "HR")
    role_menu.grid(row=6, column=1)

    tk.Label(add_window, text="Password").grid(row=7, column=0)
    password_entry = tk.Entry(add_window, show="*")
    password_entry.grid(row=7, column=1)

    tk.Button(add_window, text="Save", command=save_employee).grid(row=8, column=0, columnspan=2)

def update_employee_form(tree):
    def save_updated_employee():
        payroll_number = payroll_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        work_email = email_entry.get()
        contact_info = contact_entry.get()
        department = department_var.get()
        role = role_var.get()
        password = password_entry.get()

        if not payroll_number:
            messagebox.showerror("Error", "Payroll number is required.")
            return

        try:
            update_employee(payroll_number, first_name, last_name, work_email, contact_info, department, role, password)
            messagebox.showinfo("Success", "Employee updated successfully!")
            update_window.destroy()
            display_employees(tree)  # Update the Treeview dynamically
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", "An error occurred while updating the employee. Please try again.")

    update_window = tk.Toplevel()
    update_window.title("Update Employee")

    tk.Label(update_window, text="Payroll Number").grid(row=0, column=0)
    payroll_entry = tk.Entry(update_window)
    payroll_entry.grid(row=0, column=1)

    tk.Label(update_window, text="First Name").grid(row=1, column=0)
    first_name_entry = tk.Entry(update_window)
    first_name_entry.grid(row=1, column=1)

    tk.Label(update_window, text="Last Name").grid(row=2, column=0)
    last_name_entry = tk.Entry(update_window)
    last_name_entry.grid(row=2, column=1)

    tk.Label(update_window, text="Work Email").grid(row=3, column=0)
    email_entry = tk.Entry(update_window)
    email_entry.grid(row=3, column=1)

    tk.Label(update_window, text="Contact Info").grid(row=4, column=0)
    contact_entry = tk.Entry(update_window)
    contact_entry.grid(row=4, column=1)

    tk.Label(update_window, text="Department").grid(row=5, column=0)
    department_var = tk.StringVar()
    department_menu = tk.OptionMenu(update_window, department_var, "IT", "HR", "Finance", "Legal", "Marketing")
    department_menu.grid(row=5, column=1)

    tk.Label(update_window, text="Role").grid(row=6, column=0)
    role_var = tk.StringVar()
    role_menu = tk.OptionMenu(update_window, role_var, "Employee", "HR")
    role_menu.grid(row=6, column=1)

    tk.Label(update_window, text="Password").grid(row=7, column=0)
    password_entry = tk.Entry(update_window, show="*")
    password_entry.grid(row=7, column=1)

    tk.Button(update_window, text="Save", command=save_updated_employee).grid(row=8, column=0, columnspan=2)

def delete_employee_prompt(tree):
    def confirm_delete():
        payroll_number = payroll_entry.get()
        if not payroll_number:
            messagebox.showerror("Error", "Payroll number is required.")
            return

        delete_employee(payroll_number)
        messagebox.showinfo("Success", f"Employee {payroll_number} deleted successfully!")
        delete_window.destroy()
        display_employees(tree)  # Update the Treeview dynamically

    delete_window = tk.Toplevel()
    delete_window.title("Delete Employee")

    tk.Label(delete_window, text="Payroll Number").grid(row=0, column=0)
    payroll_entry = tk.Entry(delete_window)
    payroll_entry.grid(row=0, column=1)

    tk.Button(delete_window, text="Delete", command=confirm_delete).grid(row=1, column=0, columnspan=2)

def view_employees(tree):
    columns, employees = view_employees_data()

    # Clear the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Update Treeview columns
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, minwidth=100)

    # Insert data into the Treeview
    for employee in employees:
        tree.insert("", tk.END, values=employee)

def hr_dashboard(user_details):
    # Create the main window
    root = tk.Tk()
    root.title("HR Dashboard")
    root.geometry("800x600")

    # HR Info Display
    tk.Label(root, text=f"Welcome, {user_details['first_name']} {user_details['last_name']}", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text=f"Role: {user_details['role']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(root, text=f"Email: {user_details['work_email']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(root, text=f"Department: {user_details['department']}", font=("Arial", 12)).pack(pady=5)

    # Search and Filter Frame
    search_filter_frame = tk.Frame(root)
    search_filter_frame.pack(pady=10)

    # Search Bar
    search_label = tk.Label(search_filter_frame, text="Search Employees:", font=("Arial", 12))
    search_label.pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_filter_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    # Filter by Department
    department_filter_var = tk.StringVar()
    department_filter_menu = tk.OptionMenu(search_filter_frame, department_filter_var, "All", "IT", "HR", "Finance", "Legal", "Marketing")
    department_filter_menu.pack(side=tk.LEFT, padx=5)
    department_filter_var.set("All")

    # Filter by Role
    role_filter_var = tk.StringVar()
    role_filter_menu = tk.OptionMenu(search_filter_frame, role_filter_var, "All", "Employee", "HR")
    role_filter_menu.pack(side=tk.LEFT, padx=5)
    role_filter_var.set("All")

    # Button for searching
    search_button = tk.Button(search_filter_frame, text="Search", command=lambda: search_button_click())
    search_button.pack(side=tk.LEFT, padx=5)

    # Treeview for displaying employee data
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side='right', fill='y')
    hsb.pack(side='bottom', fill='x')

    # Button for searching
    def search_button_click():
        department_filter = department_filter_var.get()
        role_filter = role_filter_var.get()
        if department_filter == "All":
            department_filter = None
        if role_filter == "All":
            role_filter = None
        display_employees(tree, search_entry.get(), department_filter, role_filter)

    # Frame for employee management buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Buttons for employee management
    tk.Button(button_frame, text="Add New Employee", width=20, command=lambda: add_employee_form(tree)).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Edit Employee", width=20, command=lambda: update_employee_form(tree)).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Remove Employee", width=20, command=lambda: delete_employee_prompt(tree)).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="View Employees", width=20, command=lambda: view_employees(tree)).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Import Employees", width=20, command=lambda: import_employees(tree)).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Export Employees", width=20, command=export_employees).grid(row=1, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Logout", width=20, command=root.destroy).grid(row=2, column=1, padx=5, pady=5)

    root.mainloop()
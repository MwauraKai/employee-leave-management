import sqlite3
import tkinter as tk

def display_employees(tree, search_term="", department_filter=None, role_filter=None):
    # Clear the Treeview
    for row in tree.get_children():
        tree.delete(row)

    employees = search_employees(search_term, department_filter, role_filter)

    # Fetch column names
    columns, _ = view_employees_data()
    tree["columns"] = columns

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, minwidth=100)

    for employee in employees:
        tree.insert("", tk.END, values=employee)

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

def view_employees_data():
    with sqlite3.connect("employee_system.db") as conn:
        cursor = conn.cursor()

        # Fetch column names
        cursor.execute("PRAGMA table_info(employees);")
        columns = [col[1] for col in cursor.fetchall()]  # Extract column names

        # Fetch all employee data
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

    return columns, employees
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from tkcalendar import DateEntry

# Function to fetch leave requests
def fetch_leave_requests(start_date=None, end_date=None, payroll_number=None, status=None, department=None):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    
    query = """
        SELECT lr.id, e.payroll_number, e.first_name, e.last_name, lr.leave_type, lr.start_date, lr.end_date, lr.reason, lr.status, e.department
        FROM leave_requests lr
        JOIN employees e ON lr.employee_id = e.id
    """
    params = []
    conditions = []

    if start_date and end_date:
        conditions.append("date(lr.start_date) BETWEEN ? AND ?")
        params.extend([start_date, end_date])
    if payroll_number:
        conditions.append("e.payroll_number = ?")
        params.append(payroll_number)
    if status:
        conditions.append("lr.status = ?")
        params.append(status)
    if department:
        conditions.append("e.department = ?")
        params.append(department)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY lr.start_date DESC"
    cursor.execute(query, params)
    records = cursor.fetchall()
    
    conn.close()
    return records

# Function to update leave request status
def update_leave_status(tree, new_status):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No leave request selected.")
        return
    
    leave_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE leave_requests SET status = ? WHERE id = ?", (new_status, leave_id))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Leave request updated successfully!")
    update_leave_treeview(tree)

# Function to update the Treeview with leave requests
def update_leave_treeview(tree, start_date=None, end_date=None, payroll_number=None, status=None, department=None):
    for row in tree.get_children():
        tree.delete(row)
    records = fetch_leave_requests(start_date, end_date, payroll_number, status, department)
    for record in records:
        tree.insert("", tk.END, values=record)

# Leave Management Dashboard function
def leave_dashboard(user_details):
    root = tk.Tk()
    root.title("Leave Management Dashboard")
    root.geometry("700x600")

    tk.Label(root, text=f"Welcome, {user_details['first_name']} {user_details['last_name']}", font=("Arial", 14)).pack(pady=10)
    
    # Buttons Frame at the Top
    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.X, padx=10, pady=5)
    
    approve_button = tk.Button(button_frame, text="Approve", command=lambda: update_leave_status(leave_tree, "approved"))
    approve_button.pack(side=tk.LEFT, padx=5)
    
    reject_button = tk.Button(button_frame, text="Reject", command=lambda: update_leave_status(leave_tree, "rejected"))
    reject_button.pack(side=tk.LEFT, padx=5)
    
    logout_btn = tk.Button(button_frame, text="Logout", command=root.destroy)
    logout_btn.pack(side=tk.RIGHT, padx=5)
    
    # Main Frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    leave_frame = tk.Frame(main_frame)
    leave_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=7, pady=7)

    tk.Label(leave_frame, text="Leave Requests", font=("Arial", 12)).pack(pady=7)
    
    tree_frame = tk.Frame(leave_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    leave_tree = ttk.Treeview(tree_frame, columns=("ID", "Payroll Number", "First Name", "Last Name", "Leave Type", "Start Date", "End Date", "Reason", "Status", "Department"), show="headings", height=8)

    for col in ("ID", "Payroll Number", "First Name", "Last Name", "Leave Type", "Start Date", "End Date", "Reason", "Status", "Department"):
        leave_tree.heading(col, text=col)
        leave_tree.column(col, width=80)
        

    leave_v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=leave_tree.yview)
    leave_tree.configure(yscrollcommand=leave_v_scroll.set)
    leave_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    leave_h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=leave_tree.xview)
    leave_tree.configure(xscrollcommand=leave_h_scroll.set)
    leave_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    leave_tree.pack(fill=tk.BOTH, expand=True)
    update_leave_treeview(leave_tree)

    # Filter Section
    leave_filter_frame = tk.Frame(main_frame)
    leave_filter_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(leave_filter_frame, text="Filter Leave Requests", font=("Arial", 12)).pack(pady=10)
    tk.Label(leave_filter_frame, text="Start Date").pack()
    leave_filter_start_date_entry = DateEntry(leave_filter_frame, date_pattern='yyyy-mm-dd')
    leave_filter_start_date_entry.pack(pady=5)
    
    tk.Label(leave_filter_frame, text="End Date").pack()
    leave_filter_end_date_entry = DateEntry(leave_filter_frame, date_pattern='yyyy-mm-dd')
    leave_filter_end_date_entry.pack(pady=5)
    
    tk.Label(leave_filter_frame, text="Payroll Number").pack()
    leave_filter_payroll_number_entry = tk.Entry(leave_filter_frame)
    leave_filter_payroll_number_entry.pack(pady=5)
    
    tk.Label(leave_filter_frame, text="Status").pack()
    leave_filter_status_var = tk.StringVar()
    leave_filter_status_menu = tk.OptionMenu(leave_filter_frame, leave_filter_status_var, "All", "pending", "approved", "rejected")
    leave_filter_status_menu.pack(pady=10)
    leave_filter_status_var.set("All")

    tk.Label(leave_filter_frame, text="Department").pack()
    leave_filter_department_var = tk.StringVar()
    leave_filter_department_menu = tk.OptionMenu(leave_filter_frame, leave_filter_department_var, "All", "IT", "HR", "Finance", "Legal", "Marketing",'Supply Chain')
    leave_filter_department_menu.pack(pady=10)
    leave_filter_department_var.set("All")
    
    leave_filter_button = tk.Button(leave_filter_frame, text="Filter", command=lambda: update_leave_treeview(
        leave_tree,
        leave_filter_start_date_entry.get(),
        leave_filter_end_date_entry.get(),
        leave_filter_payroll_number_entry.get(),
        None if leave_filter_status_var.get() == "All" else leave_filter_status_var.get(),
        None if leave_filter_department_var.get() == "All" else leave_filter_department_var.get()
    ))
    leave_filter_button.pack(pady=5)

    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

# Function to record attendance
def record_attendance(employee_id, event_type):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO attendance (employee_id, event_type, timestamp) VALUES (?, ?, ?)", (employee_id, event_type, timestamp))
    
    conn.commit()
    conn.close()

# Function to fetch attendance data
def fetch_attendance(employee_id, start_date=None, end_date=None):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    
    query = "SELECT event_type, timestamp FROM attendance WHERE employee_id = ?"
    params = [employee_id]
    
    if start_date and end_date:
        query += " AND date(timestamp) BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    
    query += " ORDER BY timestamp DESC"
    cursor.execute(query, params)
    records = cursor.fetchall()
    
    conn.close()
    return records

# Function to update the Treeview with attendance records
def update_treeview(tree, employee_id, start_date=None, end_date=None):
    # Clear the Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    # Fetch new attendance data and insert into Treeview
    records = fetch_attendance(employee_id, start_date, end_date)
    for record in records:
        tree.insert("", tk.END, values=record)

# Function to submit leave request
def submit_leave_request(employee_id, leave_tree):
    def save_leave_request():
        leave_type = leave_type_var.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        reason = reason_entry.get("1.0", tk.END).strip()

        if not leave_type or not start_date or not end_date or not reason:
            messagebox.showerror("Error", "All fields are required.")
            return

        if leave_type not in ['Annual', 'Sick', 'Unpaid', 'Maternity', 'Paternity']:
            messagebox.showerror("Error", "Invalid leave type.")
            return

        try:
            conn = sqlite3.connect("employee_system.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason, status) VALUES (?, ?, ?, ?, ?, ?)",
                           (employee_id, leave_type, start_date, end_date, reason, "pending"))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Leave request submitted successfully!")
            leave_window.destroy()
            update_leave_treeview(leave_tree, employee_id)  # Update the leave requests Treeview dynamically
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            conn.close()

    leave_window = tk.Toplevel()
    leave_window.title("Submit Leave Request")

    tk.Label(leave_window, text="Leave Type").grid(row=0, column=0)
    leave_type_var = tk.StringVar()
    leave_type_menu = tk.OptionMenu(leave_window, leave_type_var, "Annual", "Sick", "Unpaid", "Maternity", "Paternity")
    leave_type_menu.grid(row=0, column=1)

    tk.Label(leave_window, text="Start Date").grid(row=1, column=0)
    start_date_entry = DateEntry(leave_window, date_pattern='yyyy-mm-dd')
    start_date_entry.grid(row=1, column=1)

    tk.Label(leave_window, text="End Date").grid(row=2, column=0)
    end_date_entry = DateEntry(leave_window, date_pattern='yyyy-mm-dd')
    end_date_entry.grid(row=2, column=1)

    tk.Label(leave_window, text="Reason").grid(row=3, column=0)
    reason_entry = tk.Text(leave_window, width=30, height=5)
    reason_entry.grid(row=3, column=1)

    tk.Button(leave_window, text="Submit", command=save_leave_request).grid(row=4, column=0, columnspan=2)

# Function to fetch leave requests
def fetch_leave_requests(employee_id, start_date=None, end_date=None):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    
    query = "SELECT leave_type, start_date, end_date, reason, status FROM leave_requests WHERE employee_id = ?"
    params = [employee_id]
    
    if start_date and end_date:
        query += " AND date(start_date) BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    
    query += " ORDER BY start_date DESC"
    cursor.execute(query, params)
    records = cursor.fetchall()
    
    conn.close()
    return records

# Function to update the Treeview with leave requests
def update_leave_treeview(tree, employee_id, start_date=None, end_date=None):
    # Clear the Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    # Fetch new leave request data and insert into Treeview
    records = fetch_leave_requests(employee_id, start_date, end_date)
    for record in records:
        tree.insert("", tk.END, values=record)

# Function to fetch remaining leave days
def fetch_remaining_leave_days(employee_id):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT leave_type, COUNT(*) FROM leave_requests WHERE employee_id = ? AND status = 'approved' GROUP BY leave_type", (employee_id,))
    records = cursor.fetchall()
    
    conn.close()
    return records

# Employee dashboard function
def employee_dashboard(employee_id, employee_name):
    root = tk.Tk()
    root.title("Employee Dashboard")
    root.geometry("1000x600")

    # Welcome message
    tk.Label(root, text=f"Welcome, {employee_name}", font=("Arial", 14)).pack(pady=10)

    # Frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Clock In and Clock Out Buttons
    clock_in_btn = tk.Button(button_frame, text="Clock In", width=20, command=lambda: [record_attendance(employee_id, "clock_in"), update_treeview(attendance_tree, employee_id)])
    clock_in_btn.grid(row=0, column=0, padx=5)
    
    clock_out_btn = tk.Button(button_frame, text="Clock Out", width=20, command=lambda: [record_attendance(employee_id, "clock_out"), update_treeview(attendance_tree, employee_id)])
    clock_out_btn.grid(row=0, column=1, padx=5)
    
    # Submit Leave Request Button
    leave_btn = tk.Button(button_frame, text="Submit Leave Request", width=20, command=lambda: submit_leave_request(employee_id, leave_tree))
    leave_btn.grid(row=0, column=2, padx=5)

    # Frame for attendance history and filters
    attendance_frame = tk.Frame(root)
    attendance_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Attendance Treeview
    tk.Label(attendance_frame, text="Attendance History", font=("Arial", 12)).pack(pady=10)
    attendance_tree = ttk.Treeview(attendance_frame, columns=("Event", "Timestamp"), show="headings", height=8)
    attendance_tree.heading("Event", text="Event Type")
    attendance_tree.heading("Timestamp", text="Timestamp")
    update_treeview(attendance_tree, employee_id)
    attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar for attendance Treeview
    attendance_scrollbar = ttk.Scrollbar(attendance_frame, orient="vertical", command=attendance_tree.yview)
    attendance_tree.configure(yscrollcommand=attendance_scrollbar.set)
    attendance_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    # Attendance Filter Frame
    filter_frame = tk.Frame(attendance_frame)
    filter_frame.pack(side=tk.LEFT, padx=10)

    tk.Label(filter_frame, text="Filter Attendance Records", font=("Arial", 12)).pack(pady=10)
    tk.Label(filter_frame, text="Start Date").pack()
    filter_start_date_entry = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
    filter_start_date_entry.pack(pady=5)
    
    tk.Label(filter_frame, text="End Date").pack()
    filter_end_date_entry = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
    filter_end_date_entry.pack(pady=5)
    
    filter_button = tk.Button(filter_frame, text="Filter", command=lambda: update_treeview(attendance_tree, employee_id, filter_start_date_entry.get(), filter_end_date_entry.get()))
    filter_button.pack(pady=5)

    # Frame for leave request history and filters
    leave_frame = tk.Frame(root)
    leave_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Leave Request Treeview
    tk.Label(leave_frame, text="Leave Request History", font=("Arial", 12)).pack(pady=10)
    leave_tree = ttk.Treeview(leave_frame, columns=("Leave Type", "Start Date", "End Date", "Reason", "Status"), show="headings", height=8)
    leave_tree.heading("Leave Type", text="Leave Type")
    leave_tree.heading("Start Date", text="Start Date")
    leave_tree.heading("End Date", text="End Date")
    leave_tree.heading("Reason", text="Reason")
    leave_tree.heading("Status", text="Status")
    update_leave_treeview(leave_tree, employee_id)
    leave_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar for leave Treeview
    leave_scrollbar = ttk.Scrollbar(leave_frame, orient="vertical", command=leave_tree.yview)
    leave_tree.configure(yscrollcommand=leave_scrollbar.set)
    leave_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    # Leave Filter Frame
    leave_filter_frame = tk.Frame(leave_frame)
    leave_filter_frame.pack(side=tk.LEFT, padx=10)

    tk.Label(leave_filter_frame, text="Filter Leave Requests", font=("Arial", 12)).pack(pady=10)
    tk.Label(leave_filter_frame, text="Start Date").pack()
    leave_filter_start_date_entry = DateEntry(leave_filter_frame, date_pattern='yyyy-mm-dd')
    leave_filter_start_date_entry.pack(pady=5)
    
    tk.Label(leave_filter_frame, text="End Date").pack()
    leave_filter_end_date_entry = DateEntry(leave_filter_frame, date_pattern='yyyy-mm-dd')
    leave_filter_end_date_entry.pack(pady=5)
    
    leave_filter_button = tk.Button(leave_filter_frame, text="Filter", command=lambda: update_leave_treeview(leave_tree, employee_id, leave_filter_start_date_entry.get(), leave_filter_end_date_entry.get()))
    leave_filter_button.pack(pady=5)

    # Remaining Leave Days
    tk.Label(root, text="Remaining Leave Days", font=("Arial", 12)).pack(pady=10)
    remaining_leave_days = fetch_remaining_leave_days(employee_id)
    for leave_type, count in remaining_leave_days:
        tk.Label(root, text=f"{leave_type}: {count} days").pack()

    # Logout Button
    logout_btn = tk.Button(root, text="Logout", width=20, command=root.destroy)
    logout_btn.pack(pady=20)

    root.mainloop()
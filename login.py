import tkinter as tk
from tkinter import messagebox
import sqlite3
from employee_views import employee_dashboard
from hr_views import hr_dashboard
from leave_views import leave_dashboard

# Function to authenticate user
def authenticate_user(email, password):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE work_email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    
    if user:
        user_id = user[0]
        first_name = user[2]
        last_name = user[3]
        role = user[7]  # Assuming index 7 is the role
        department = user[8]  # Assuming index 8 is the department
        return user_id, first_name, last_name, role, department  # Returning user data and role
    else:
        return None, None, None, None, None

def login():
    email = email_entry.get()
    password = password_entry.get()

    user_id, first_name, last_name, role, department = authenticate_user(email, password)

    if user_id:
        # Login successful
        messagebox.showinfo("Login Successful", f"Welcome {first_name} {last_name} ({role})")

        if remember_me_var.get():
            with open("remember_me.txt", "w") as f:
                f.write(email)
        else:
            with open("remember_me.txt", "w") as f:
                f.write("")

        root.withdraw()  # Instead of destroy(), hide login window

        if role == 'Employee':
            employee_dashboard(user_id, f"{first_name} {last_name}")  
        elif role == 'HR':
            choose_dashboard(user_id, first_name, last_name, role, email, department)
    else:
        # Invalid credentials
        messagebox.showerror("Login Failed", "Invalid email or password.")


# Function to prompt HR to choose dashboard
def choose_dashboard(user_id, first_name, last_name, role, email, department):
    def open_hr_dashboard():
        choose_window.destroy()
        hr_dashboard({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'role': role, 'work_email': email, 'department': department})

    def open_leave_dashboard():
        choose_window.destroy()
        leave_dashboard({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'role': role, 'work_email': email, 'department': department})

    choose_window = tk.Toplevel()
    choose_window.title("Choose Dashboard")
    choose_window.geometry("300x150")

    tk.Label(choose_window, text="Choose Dashboard", font=("Arial", 14)).pack(pady=10)
    tk.Button(choose_window, text="Employee Management", command=open_hr_dashboard).pack(pady=5)
    tk.Button(choose_window, text="Leave Management", command=open_leave_dashboard).pack(pady=5)

# Function to show the forgot password window
def forgot_password():
    def send_recovery_email():
        email = email_entry.get()
        # Here you would implement the logic to send a recovery email
        messagebox.showinfo("Forgot Password", f"Password recovery instructions have been sent to {email}")
        forgot_password_window.destroy()

    forgot_password_window = tk.Toplevel()
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("300x150")

    tk.Label(forgot_password_window, text="Enter your email:").pack(pady=5)
    email_entry = tk.Entry(forgot_password_window, width=30)
    email_entry.pack(pady=5)

    send_button = tk.Button(forgot_password_window, text="Send", command=send_recovery_email)
    send_button.pack(pady=10)

# Creating the Tkinter root window for login
root = tk.Tk()
root.title("Login")

# Create the email label and entry
email_label = tk.Label(root, text="Email:")
email_label.pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack(pady=5)

# Create the password label and entry
password_label = tk.Label(root, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(root, width=30, show="*")  # show="*" hides password
password_entry.pack(pady=5)

# Remember Me checkbox
remember_me_var = tk.IntVar()
remember_me_check = tk.Checkbutton(root, text="Remember Me", variable=remember_me_var)
remember_me_check.pack(pady=5)

# Create the login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

# Forgot Password button
forgot_password_button = tk.Button(root, text="Forgot Password", command=forgot_password)
forgot_password_button.pack(pady=5)

# Pre-fill email if "Remember Me" was checked
try:
    with open("remember_me.txt", "r") as f:
        saved_email = f.read().strip()
        if saved_email:
            email_entry.insert(0, saved_email)
            remember_me_var.set(1)
except FileNotFoundError:
    pass

# Start the Tkinter event loop for the login window
root.mainloop()
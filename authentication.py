import sqlite3
from tkinter import messagebox

def authenticate_user(email, password):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()

    # Query to check if the email and password match in the database
    cursor.execute("SELECT * FROM employees WHERE work_email = ? AND password = ?", (email, password))
    user = cursor.fetchone()

    if user:
        # Extracting user info (you can access these based on the column index)
        user_details = {
            "id": user[0],
            "payroll_number": user[1],
            "first_name": user[2],
            "last_name": user[3],
            "work_email": user[4],
            "contact_info": user[5],
            "department": user[6],
            "role": user[7],  # Assuming index 7 is the role
            "leave_entitlement": user[8],
            "current_leave_balance": user[9]
        }
        print(f"Login successful for {user_details['first_name']} {user_details['last_name']} ({user_details['role']})")
        return user_details  # Returning user details for further use (such as dashboard navigation)
    else:
        messagebox.showerror("Login Failed", "Invalid email or password.")
        return None
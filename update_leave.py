import sqlite3
from tkinter import messagebox

def update_leave_status(leave_id, new_status):
    """
    Function to update the status of a leave request in the database.
    :param leave_id: ID of the leave request
    :param new_status: New status ('Approved', 'Rejected', etc.)
    """
    try:
        with sqlite3.connect("employee_system.db") as conn:
            cursor = conn.cursor()
            
            # Check if leave request exists
            cursor.execute("SELECT * FROM leave_requests WHERE leave_id = ?", (leave_id,))
            leave_request = cursor.fetchone()
            
            if not leave_request:
                messagebox.showerror("Error", f"No leave request found with ID {leave_id}.")
                return
            
            # Update leave request status
            cursor.execute("UPDATE leave_requests SET status = ? WHERE leave_id = ?", (new_status, leave_id))
            conn.commit()
            messagebox.showinfo("Success", f"Leave request {leave_id} updated to {new_status}!")
    
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error updating leave status: {e}")

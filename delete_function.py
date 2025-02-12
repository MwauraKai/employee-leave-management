# Function to delete an employee from the database.
import sqlite3
def delete_employee(payroll_number):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()

    # Check if employee exists
    cursor.execute("SELECT * FROM employees WHERE payroll_number = ?", (payroll_number,))
    existing_employee = cursor.fetchone()

    if not existing_employee:
        print(f"Employee with payroll number {payroll_number} not found!")
    else:
        cursor.execute("DELETE FROM employees WHERE payroll_number = ?", (payroll_number,))
        conn.commit()
        print(f"Employee {payroll_number} deleted successfully!")

    conn.close()

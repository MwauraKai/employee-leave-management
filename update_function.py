
#Function to update employee details in the database.

import sqlite3
def update_employee(payroll_number, first_name=None, last_name=None, work_email=None, contact_info=None, department=None, role=None, password=None):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()

    # Check if employee exists
    cursor.execute("SELECT * FROM employees WHERE payroll_number = ?", (payroll_number,))
    existing_employee = cursor.fetchone()

    if not existing_employee:
        print(f"Employee with payroll number {payroll_number} not found!")
        conn.close()
        return

    # Build the update query dynamically
    update_fields = []
    values = []

    if first_name:
        update_fields.append("first_name = ?")
        values.append(first_name)
    if last_name:
        update_fields.append("last_name = ?")
        values.append(last_name)
    if work_email:
        update_fields.append("work_email = ?")
        values.append(work_email)
    if contact_info:
        update_fields.append("contact_info = ?")
        values.append(contact_info)
    if department:
        update_fields.append("department = ?")
        values.append(department)
    if role:
        update_fields.append("role = ?")
        values.append(role)
    if password:
        update_fields.append("password = ?")
        values.append(password)

    # Ensure we have something to update
    if update_fields:
        update_query = f"UPDATE employees SET {', '.join(update_fields)} WHERE payroll_number = ?"
        values.append(payroll_number)

        cursor.execute(update_query, values)
        conn.commit()
        print(f"Employee {payroll_number} updated successfully!")
    conn.close()
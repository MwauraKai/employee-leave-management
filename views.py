import sqlite3

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
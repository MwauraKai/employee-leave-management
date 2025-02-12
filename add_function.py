import sqlite3

def add_employee(payroll_number, first_name, last_name, work_email, contact_info, department, role, password):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO employees (payroll_number, first_name, last_name, work_email, contact_info, department, role, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (payroll_number, first_name, last_name, work_email, contact_info, department, role, password))
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
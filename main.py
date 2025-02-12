from add_function  import add_employee
# Add a test employee
add_employee('IMC1234', 'Peter', 'Adams', 'peter.adams@example.com', '0791234567', 'Supply Chain', 'Employee', 'testp123ass')

add_employee('XY120', 'Paulina', 'Nyokabi', 'eve.nyoksds@example.com', '0791125567', 'Legal', 'HR', 'testingss')


from update_function import update_employee
update_employee('XYZ789',last_name='Peter')

from delete_function import delete_employee
delete_employee('XYZ2000')

from views import view_employees_data
view_employees_data()
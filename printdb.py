from persistence import *

def print_activities():
    """Display the activities table, ordered by the date"""
    activities = repo.activities.find_all()
    order_activities = sorted(activities, key=lambda x: x.date)
    #print the activitie orderd by date
    print("Activities")
    for activitie in order_activities:
        print(activitie)
    

def print_branches():
    """Display the branches table, ordered by the ID"""
    branchs = repo.branches.find_all()
    order_branchs = sorted(branchs, key=lambda x: x.id)
    #print the branch orderd by id
    print("Branches")
    for branch in order_branchs:
        print(branch)

def print_employees():
    """Display the employees table, ordered by the ID"""
    employees = repo.employees.find_all()
    order_employees = sorted(employees, key=lambda x: x.id)
    #print the branch orderd by id
    print("Employees")
    for employee in order_employees:
        print(employee)

def print_products():
    """Display the products table, ordered by the ID"""
    products = repo.products.find_all()
    order_products = sorted(products, key=lambda x: x.id)
    #print the branch orderd by id
    print("Products")
    for product in order_products:
        print(product)


def print_suppliers():
    """Print the suppliers table ordered by ID."""
    suppliers = repo.suppliers.find_all()
    order_suppliers = sorted(suppliers, key=lambda x: x.id)
    #print the branch orderd by id
    print("Suppliers")
    for supplier in order_suppliers:
        print(supplier)


def print_detailed_employees_report():
    print("Employees report")
    query = """
    SELECT e.name, e.salary, b.location, 
           COALESCE(SUM(p.price * ABS(a.quantity)), 0) AS total_sales_income  -- שימוש ב-ABS להפיכת כמות שלילית לחיובית
    FROM employees e
    JOIN branches b ON e.branche = b.id
    LEFT JOIN activities a ON e.id = a.activator_id AND a.quantity < 0
    LEFT JOIN products p ON a.product_id = p.id
    GROUP BY e.id
    ORDER BY e.name
    """
    for row in repo.execute_command(query):
        print(f"{row[0]} {row[1]} {row[2]} {row[3]}")


def print_detailed_activities_report():
    print("Activities report")
    query = """
    SELECT a.date, p.description, a.quantity,
           CASE WHEN a.quantity < 0 THEN e.name ELSE NULL END as seller,
           CASE WHEN a.quantity > 0 THEN s.name ELSE NULL END as supplier
    FROM activities a
    LEFT JOIN products p ON a.product_id = p.id
    LEFT JOIN employees e ON a.activator_id = e.id AND a.quantity < 0
    LEFT JOIN suppliers s ON a.activator_id = s.id AND a.quantity > 0
    ORDER BY a.date
    """
    
    results = repo.execute_command(query)
    
    for row in results:
        # Converting None values to explicit None for formatting consistency
        formatted_row = tuple(value if value is not None else None for value in row)
        print(formatted_row)



def main():
    print_activities()
    print_branches()
    print_employees()
    print_products()
    print_suppliers()
    print_detailed_employees_report()
    print_detailed_activities_report()


if __name__ == '__main__':
    main()
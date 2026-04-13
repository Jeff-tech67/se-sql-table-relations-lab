# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd 

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql(
    """
    SELECT e.firstName,
           e.lastName
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
    """,
    conn,
)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql(
    """
    SELECT o.officeCode,
           o.city,
           COUNT(e.employeeNumber) AS emp_count
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    GROUP BY o.officeCode, o.city
    HAVING emp_count = 0
    """,
    conn,
)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql(
    """
    SELECT e.firstName,
           e.lastName,
           o.city,
           o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
    """,
    conn,
)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql(
    """
    SELECT c.contactFirstName,
           c.contactLastName,
           c.phone,
           c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
    """,
    conn,
)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql(
    """
    SELECT c.contactFirstName,
           c.contactLastName,
           p.paymentDate,
           p.amount
    FROM payments p
    JOIN customers c ON p.customerNumber = c.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
    """,
    conn,
)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql(
    """
    SELECT e.employeeNumber,
           e.firstName,
           e.lastName,
           COUNT(c.customerNumber) AS num_customers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
    ORDER BY num_customers DESC
    """,
    conn,
)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql(
    """
    SELECT p.productName,
           COUNT(od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productName
    ORDER BY totalunits DESC
    """,
    conn,
)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql(
    """
    SELECT p.productName,
           p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
    """,
    conn,
)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql(
    """
    SELECT COUNT(DISTINCT c.customerNumber) AS n_customers,
           e.officeCode,
           o.city
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN offices o ON e.officeCode = o.officeCode
    GROUP BY e.officeCode, o.city
    ORDER BY e.officeCode
    """,
    conn,
)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql(
    """
    WITH underperforming AS (
        SELECT od.productCode
        FROM orderdetails od
        JOIN orders o ON od.orderNumber = o.orderNumber
        GROUP BY od.productCode
        HAVING COUNT(DISTINCT o.customerNumber) < 20
    )
    SELECT DISTINCT e.employeeNumber,
                    e.firstName,
                    e.lastName,
                    o.city,
                    e.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
    JOIN orders ord ON ord.customerNumber = c.customerNumber
    JOIN orderdetails od ON od.orderNumber = ord.orderNumber
    JOIN underperforming u ON od.productCode = u.productCode
    ORDER BY e.lastName, e.firstName
    """,
    conn,
)

conn.close()
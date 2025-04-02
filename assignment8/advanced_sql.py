import datetime
import sqlite3
import traceback


def print_exception_info(e):
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")


def print_result(result, message):
    print(message)
    for row in result:
        print(row)


with sqlite3.connect("../db/lesson.db") as conn:
    try:
        conn.execute("PRAGMA foreign_keys = 1")

        cursor = conn.cursor()

        # Task 1: Understanding Subqueries
        sql_statement = """
            SELECT o.order_id, li.line_item_id, p.product_name
            FROM products p
            JOIN line_items li ON li.product_id = p.product_id
            JOIN orders o ON o.order_id = li.order_id
            WHERE o.order_id IN (SELECT order_id id
                                 FROM orders
                                 ORDER BY order_id
                                 LIMIT 5)
        """
        cursor.execute(sql_statement)
        print_result(cursor.fetchall(), "Task 1: Understanding Subqueries")

        # Task 2: Complex JOINs with Aggregation
        sql_statement = """
            SELECT o.order_id, SUM(li.quantity * p.price) as total_price
            FROM products p
            JOIN line_items li ON li.product_id = p.product_id
            JOIN orders o ON o.order_id = li.order_id
            GROUP BY o.order_id
            ORDER BY o.order_id
            LIMIT 5
        """
        cursor.execute(sql_statement)
        print_result(cursor.fetchall(), "Task 2: Complex JOINs with Aggregation")

        # Task 3: An Insert Transaction Based on Data
        try:
            customer_id = cursor.execute("""
                    SELECT customer_id
                    FROM customers
                    WHERE customer_name = 'Perez and Sons'
                """).fetchone()[0]
            employee_id = cursor.execute("""
                    SELECT employee_id
                    FROM employees
                    WHERE first_name = 'Miranda' AND last_name = 'Harris'
                """).fetchone()[0]
            product_ids = cursor.execute("""
                    SELECT product_id
                    FROM products
                    ORDER BY price
                    LIMIT 5
                """).fetchall()

            print("Inserting data into orders")
            order_id = cursor.execute(
                "INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, ?)",
                [customer_id, employee_id, datetime.datetime.isoformat(datetime.datetime.now())]
            ).lastrowid
            print("Inserting data into line_items")
            for product_id in product_ids:
                cursor.execute(
                    "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                    [order_id, product_id[0], 10]
                )

            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error:", e)

        sql_statement = """
            SELECT o.order_id, li.line_item_id, li.quantity, p.product_name
            FROM products p
            JOIN line_items li ON li.product_id = p.product_id
            JOIN orders o ON o.order_id = li.order_id
            WHERE o.order_id = ?;
        """
        cursor.execute(sql_statement, (order_id,))
        print_result(cursor.fetchall(), "Task 3: An Insert Transaction Based on Data")

        # Task 4: Aggregation with HAVING
        sql_statement = """
            SELECT e.first_name, e.last_name, COUNT(o.order_id) as Total_orders
            FROM employees e
            JOIN orders o ON o.employee_id = e.employee_id
            GROUP BY e.first_name, e.last_name
            HAVING Total_orders > 5
        """
        cursor.execute(sql_statement)
        print_result(cursor.fetchall(), "Task 4: Aggregation with HAVING")
    except Exception as e:
        print(f"SQL error:")
        print_exception_info(e)

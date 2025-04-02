import pandas as pd
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

with sqlite3.connect("../db/lesson.db") as conn:
    try:
        sql_statement = """
            SELECT li.line_item_id, li.quantity, p.product_id, p.product_name, p.price
            FROM products p
            JOIN line_items li ON li.product_id = p.product_id
        """
        df = pd.read_sql_query(sql_statement, conn)
        print("Start df:")
        print(df.head(5))

        df['total'] = df['quantity'] * df['price']
        print("df with total:")
        print(df.head(5))

        grouped_df = df.groupby(["product_id"]).agg({"line_item_id": "count", "total": "sum", "product_name": "first"})
        print("grouped df:")
        print(grouped_df)

        sorted_df = grouped_df.sort_values(["product_name"])
        print("sorted by product name df:")
        print(sorted_df.head(5))

        sorted_df.to_csv("order_summary.csv")
    except Exception as e:
        print(f"SQL error:")
        print_exception_info(e)

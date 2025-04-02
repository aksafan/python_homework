import datetime
import random
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


def populate_publishers(name):
    try:
        return cursor.execute("INSERT INTO publishers (name) VALUES (?)", [name]).lastrowid
    except sqlite3.Error as e:
        print_exception_info(e)


def populate_magazines(publisher_id, name):
    try:
        return cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
                              [name, publisher_id]).lastrowid
    except sqlite3.Error as e:
        print_exception_info(e)


def populate_subscribers(name, address):
    try:
        return cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", [name, address]).lastrowid
    except sqlite3.Error as e:
        print_exception_info(e)


def populate_subscriptions(subscriber_id, magazine_id):
    try:
        return cursor.execute(
            "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
            [
                subscriber_id,
                magazine_id,
                datetime.datetime.isoformat(datetime.datetime.now() + datetime.timedelta(days=random.randrange(1, 100)))
            ]
        ).lastrowid
    except sqlite3.Error as e:
        print_exception_info(e)


# Task 1: Create a New SQLite Database
with sqlite3.connect("../db/magazines.db") as conn:
    try:
        conn.execute("PRAGMA foreign_keys = 1")

        cursor = conn.cursor()

        # Task 2: Define Database Structure

        print("Task 2: Define Database Structure")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER,
                FOREIGN KEY (publisher_id) REFERENCES publishers (id)    
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE (name, address)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY,
                magazine_id INTEGER,
                subscriber_id INTEGER,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (magazine_id) REFERENCES magazines (id),
                FOREIGN KEY (subscriber_id) REFERENCES subscribers (id)
            )
        """)
    except sqlite3.Error as e:
        print_exception_info(e)

    # Task 4: Populate Tables with Data

    print("Task 4: Populate Tables with Data")
    print("Inserting data into publishers")
    publisher_ids = []
    for name in ['Alice', 'Bob', 'Charlie']:
        publisher_ids.append(populate_publishers(name))

    print("Inserting data into magazines")
    magazine_names = ["Nature", "Cardiology", "Science"]
    magazine_ids = []
    for i, publisher_id in enumerate(publisher_ids):
        magazine_ids.append(populate_magazines(publisher_id, magazine_names[i]))

    print("Inserting data into subscribers")
    subscribers = {
        "Nature Name": "463 Meadow Court Palatine, IL 60067",
        "Cardiology Name": "368 Princess St. Fort Lee, NJ 07024",
        "Science Name": "7700 Virginia Dr. Elizabeth City, NC 27909"
    }
    subscriber_ids = []
    for name, address in subscribers.items():
        subscriber_ids.append(populate_subscribers(name, address))

    print("Inserting data into subscriptions")
    subscription_ids = []
    for i, magazine_id in enumerate(magazine_ids):
        subscription_ids.append(populate_subscriptions(subscriber_ids[i], magazine_id))

    conn.commit()

    # Task 5: Write SQL Queries

    # Write a query to retrieve all information from the subscribers table.
    cursor.execute("SELECT * FROM subscribers")
    print_result(cursor.fetchall(), "Write a query to retrieve all information from the subscribers table.")

    # Write a query to retrieve all magazines sorted by name.
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    print_result(cursor.fetchall(), "Write a query to retrieve all magazines sorted by name.")

    # Write a query to find magazines for a particular publisher, one of the publishers you created. This requires a JOIN.
    cursor.execute(
        "SELECT m.*, p.name FROM magazines m JOIN publishers p ON m.publisher_id = p.id WHERE p.name = 'Bob'")
    print_result(cursor.fetchall(),
                 "Wite a query to find magazines for a particular publisher, one of the publishers you created. This requires a JOIN.")

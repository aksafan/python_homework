import csv
import os
import traceback
import custom_module
from datetime import datetime

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

# Task 2
def read_employees():
    key_value_pairs = {}
    rows = []
    file_path = "../csv/employees.csv"

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")

        return None

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    key_value_pairs["fields"] = row
                else:
                    rows.append(row)

            key_value_pairs["rows"] = rows

        return key_value_pairs

    except Exception as e:
        print_exception_info(e)

        return None

employees = read_employees()
print(employees)

# Task 3
def column_index(input):
    return employees["fields"].index(input)

employee_id_column = column_index("employee_id")
print(employee_id_column)

# Task 4
def first_name(row_number):
    employee_id_column = column_index("first_name")

    return employees["rows"][row_number][employee_id_column]

# Task 5
def employee_find(employee_id):
    def employee_match(row):
        if employee_id_column < len(row) and row[employee_id_column] is not None and row[employee_id_column].isnumeric():
            return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))

    return matches

# Task 6
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))

    return matches

# Task 7
def sort_by_last_name():
    employees["rows"].sort(key = lambda row: row[column_index("last_name")])

    return employees["rows"]

sort_employees_rows = sort_by_last_name()
print(sort_employees_rows)

# Task 8
def employee_dict(row):
    result = dict(zip(employees["fields"], row))
    del result["employee_id"]

    return result

print(employee_dict(employees["rows"][0]))

# Task 9
def all_employees_dict():
    result = {}
    try:
        employees_rows = employees["rows"]
        iter(employees_rows)
    except IndexError:
        print("No rows in employees")

        return result
    except TypeError:
        print("employees_rows is not iterable")

        return result

    for i, row in enumerate(employees_rows):
        if len(row) > 0:
            result[row[0]] = employee_dict(employees_rows[i])

    return result

print(all_employees_dict())

# Task 10
def get_this_value():
    return os.getenv("THISVALUE")

# Task 11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("test")
print(custom_module.secret)

# Task 12
def read_minutes():
    def get_csv_content(file_path):
        key_value_pairs = {}
        rows = []

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")

            return None

        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i == 0:
                        key_value_pairs["fields"] = tuple(row)
                    else:
                        rows.append(tuple(row))

                key_value_pairs["rows"] = rows

            return key_value_pairs

        except Exception as e:
            print_exception_info(e)

            return None

    minutes1 = get_csv_content("../csv/minutes1.csv")
    minutes2 = get_csv_content("../csv/minutes2.csv")

    if not minutes1 or not minutes2:
        print("Error loading one or both CSV files.")

    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
print(minutes1, minutes2)

# Task 13
def create_minutes_set():
    minutes1, minutes2 = read_minutes()

    return set(minutes1["rows"]).union(set(minutes2["rows"]))

minutes_set = create_minutes_set()
print(minutes_set)

# Task 14
def create_minutes_list():
    minutes_set = list(create_minutes_set())

    return list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_set))

minutes_list = create_minutes_list()
print(minutes_set)

# Task 15
def write_sorted_list(file_path="minutes.csv", with_backup = False):
    minutes_list = list(create_minutes_list())
    minutes_list.sort(reverse=False, key = lambda x: x[1])
    mapped_minutes_list = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list))

    if with_backup and os.path.exists(file_path):
        backup_path = file_path + ".backup"
        print(f"Backing up existing file to {backup_path}")
        os.rename(file_path, backup_path)

    if not "fields" in minutes1:
        print("Invalid or missing minutes1_fields")

        return None

    try:
        with open(file_path, "w", newline="\n") as file:
            writer = csv.writer(file)
            writer.writerow(minutes1["fields"])
            for mapped_minute in mapped_minutes_list:
                writer.writerow(mapped_minute)

        return mapped_minutes_list

    except Exception as e:
        print_exception_info(e)

        return None

sorted_list = write_sorted_list()
print(sorted_list)

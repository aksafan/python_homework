import pandas as pd
import os

def safe_write_csv(df, file_path, with_backup = False):
    if with_backup and os.path.exists(file_path):
        try:
            backup_path = file_path + ".backup"
            print(f"Backing up existing file to {backup_path}")
            os.rename(file_path, backup_path)
        except Exception as e:
            print(f"Failed to back up file '{file_path}': {e}")

            return False

    try:
        df.to_csv(file_path, index=False)
        print(f"File saved as: {file_path}")

        return True
    except Exception as e:
        print(f"Error writing CSV to '{file_path}': {e}")

        return False

print("Task 1.1")
data = {'Name': ['Alice', 'Bob', 'charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']}
task1_data_frame = pd.DataFrame(data)
print(task1_data_frame)

print("Task 1.2")
task1_with_salary = task1_data_frame.copy()
task1_with_salary["Salary"] = [70000, 80000, 90000]
print(task1_with_salary)

print("Task 1.3")
task1_older = task1_with_salary.copy()
task1_older["Age"] += 1
print(task1_older)

print("Task 1.4")
safe_write_csv(task1_older, "employees.csv")

print("Task 2.1")
task2_employees = pd.read_csv("employees.csv")
print(task2_employees)

print("Task 2.2")
json_data = {'Name': ['Eve', 'Frank'],
             'Age': [28, 40],
             'City': ['Miami', 'Seattle'],
             'Salary': [60000, 95000]}
json_df = pd.DataFrame(json_data)
file_path = "additional_employees.json"
json_df.to_json(file_path, orient="records")
try:
    json_employees = pd.read_json(file_path, orient="records")
    print(json_employees)
except ValueError as e:
    print(f"Error reading JSON: {e}")

print("Task 2.3")
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print(more_employees)

print("Task 3.1")
first_three = more_employees.head(3)
print(first_three)

print("Task 3.2")
last_two = more_employees.tail(2)
print(last_two)

print("Task 3.3")
employee_shape = more_employees.shape
print(employee_shape)

print("Task 3.4")
print(more_employees.info)

print("Task 4.1")
dirty_data = pd.read_csv("dirty_data.csv")
print(more_employees.info)
clean_data = dirty_data.copy()

print("Task 4.2")
clean_data.drop_duplicates(inplace=True)
print(clean_data)

print("Task 4.3")
clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")
print(clean_data)

print("Task 4.4")
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors="coerce")
print(clean_data)

print("Task 4.5")
clean_data["Age"] = clean_data["Age"].fillna(clean_data["Age"].mean())
clean_data["Salary"] = clean_data["Salary"].fillna(clean_data["Age"].median())
print(clean_data)

print("Task 4.6")
clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], errors="coerce")
print(clean_data)

print("Task 4.7")
clean_data["Name"] = clean_data["Name"].str.strip()
clean_data["Name"] = clean_data["Name"].str.upper()
clean_data["Department"] = clean_data["Department"].str.strip()
clean_data["Department"] = clean_data["Department"].str.upper()
print(clean_data)

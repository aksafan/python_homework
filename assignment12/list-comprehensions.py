import pandas as pd

df = pd.read_csv("../csv/employees.csv")
employees_list = [f"{e[1].first_name} {e[1].last_name}" for e in df.iterrows()]
print(employees_list)
employees_list_with_e = [n for n in employees_list if "e" in n]
print(employees_list_with_e)

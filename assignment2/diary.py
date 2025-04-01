import csv
import traceback

# Task 1
with open("diary.txt", "a", newline="\n") as file:
    try:
        writer = csv.writer(file)
        writer.writerow(['message'])

        text_input = input("What happened today?")
        writer.writerow([text_input])

        while text_input != "done for now":
            text_input = input("What else?")
            writer.writerow([text_input])
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

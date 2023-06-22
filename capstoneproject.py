import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def reg_user():
    # Registers a new user and adds them to the user.txt file.
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")

def add_task():
    # Adds a new task to the tasks.txt file.
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            # Convert task attributes to string format
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all():
    # Displays all tasks in a formatted manner.
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine():
    # Displays tasks assigned to the current user and allows interaction.
    for i, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"Task Number: \t {i + 1}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)

            action = input("Do you want to mark this task as completed (C), edit it (E), or skip (S)? ").upper()
            if action == 'C':
                task_list[i]['completed'] = True
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in task_list:
                        # Convert task attributes to string format
                        str_attrs = [
                            t['username'],
                            t['title'],
                            t['description'],
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if t['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))
                    task_file.write("\n".join(task_list_to_write))
                print("Task marked as completed.")
            elif action == 'E':
                new_title = input("Enter a new title for the task: ")
                new_description = input("Enter a new description for the task: ")
                task_list[i]['title'] = new_title
                task_list[i]['description'] = new_description
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in task_list:
                        # Convert task attributes to string format
                        str_attrs = [
                            t['username'],
                            t['title'],
                            t['description'],
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if t['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))
                    task_file.write("\n".join(task_list_to_write))
                print("Task updated.")
            elif action == 'S':
                continue
            else:
                print("Invalid input. Task not modified.")
                continue

def display_stats():
    # Displays statistics for the number of users and tasks.
    if curr_user == "admin":
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
    else:
        print("Access denied. Only the admin user can view statistics.")

def generate_report():
    # Generates a report based on the task data.
    if curr_user == "admin":
        task_report_filename = input("Enter the task report filename (e.g., task_overview.txt): ")
        user_report_filename = input("Enter the user report filename (e.g., user_overview.txt): ")

        # Task Report
        task_report_content = ""
        for t in task_list:
            task_report_content += f"Task: {t['title']}\n"
            task_report_content += f"Assigned to: {t['username']}\n"
            task_report_content += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            task_report_content += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            task_report_content += f"Task Description:\n{t['description']}\n"
            task_report_content += f"Completed: {'Yes' if t['completed'] else 'No'}\n"
            task_report_content += "-----------------------------------\n"

        with open(task_report_filename, "w") as task_report_file:
            task_report_file.write(task_report_content)
        print("Task report generated successfully.")

        # User Report
        user_report_content = ""
        for username in username_password.keys():
            user_report_content += f"Username: {username}\n"
            user_report_content += "Tasks assigned:\n"
            user_tasks = [t for t in task_list if t['username'] == username]
            for t in user_tasks:
                user_report_content += f" - {t['title']}\n"
            user_report_content += "-----------------------------------\n"

        with open(user_report_filename, "w") as user_report_file:
            user_report_file.write(user_report_content)
        print("User report generated successfully.")
    else:
        print("Access denied. Only the admin user can generate reports.")

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
    else:
        print("Login Successful!")
        logged_in = True

while True:
    print()
    menu = input('''Select one of the following options:
r - Register a new user
a - Add a new task
va - View all tasks
vm - View my tasks
ds - Display Statistics
gr - Generate a report
e - Exit
> ''').lower()

    if menu == "r":
        reg_user()
    elif menu == "a":
        add_task()
    elif menu == "va":
        view_all()
    elif menu == "vm":
        view_mine()
    elif menu == "ds":
        display_stats()
    elif menu == "gr":
        generate_report()
    elif menu == "e":
        print("Exiting...")
        break
    else:
        print("Invalid input. Please try again.")
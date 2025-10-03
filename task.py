import json
import datetime
import os
import shlex # for parsing command line input

FILEPATH = 'data.json'

# function to add a new task
def add_task(description : str):
    """Add a new task to the task list"""
    if os.path.exists(FILEPATH):
        try:
            with open(FILEPATH, 'r') as file:
                tasks = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            tasks = []
    else: 
        tasks = []

    if tasks:
        new_id = max(task['id'] for task in tasks) + 1
    else:
        new_id = 1

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'created_at': timestamp,
        'updated_at': timestamp
        } 
    tasks.append(new_task)

    with open(FILEPATH, 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Task added successfully (ID: {new_id})")

#update task function
def update_task(task_id: int, description: str = None, status: str = None):
    """Update an existing task"""
    if not os.path.exists(FILEPATH):
        print("No tasks file found.")
        return
    with open(FILEPATH, 'r') as file:
        try:
            tasks = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            print("No tasks found.")
            return
    task_to_update = next((task for task in tasks if task["id"] == task_id), None)
    if not task_to_update:
        print(f"Task with ID {task_id} not found.")
        return
    else:
        if description:
            task_to_update['description'] = description
        if status:
            if status in ('todo', 'in-progress', 'done'):
                task_to_update['status'] = status
            else:
                print("Invalid status. Use 'todo', 'in-progress', or 'done'.")
                return
        task_to_update['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(FILEPATH, 'w') as file:
            json.dump(tasks, file, indent=4)
        print(f"Task ID {task_id} updated successfully.")


#main CLI loop
def main():
    print("Welcome to the Task Manager CLI")
    print("Type 'help' to see available commands. \n")
    while True:
        command = input("task-todo> ").strip()
        if not command:
            continue
        if command in ('exit', 'quit'):
            print("Exiting Task Manager. Goodbye!")
            break
        if command == "help":
            print("Available commands:")
            print("  add \"task description\"   → Add a new task")
            print("update <id> \"new description\" \"new status\"   → Update a task")
            print("  exit / quit              → Exit the program")
            continue
        if command.startswith("add "):
            # Extract description inside quotes
            if command.count('"') >= 2:
                description = command.split('"')[1]
                add_task(description)
            else:
                print("⚠️ Usage: add \"task description\"")
            continue
        if command.startswith("update "):
            if command.count('"') >=4:
                parts = shlex.split(command)
                try:
                    task_id = int(parts[1])
                    description = parts[2]
                    status = parts[3]
                    update_task(task_id, description, status)
                    update_task(task_id=task_id, description=description, status=status)
                except (ValueError, IndexError):
                    print("⚠️ Usage: update <id> \"new description\" \"new status\"")
            continue

        print(f"⚠️ Unknown command: {command}. Type 'help'.")

if __name__ == "__main__":
    main()


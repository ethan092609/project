import json
import os

FILENAME = "tasks.json"

# Load tasks from file if it exists
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=2)

# Display tasks
def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks yet.")
        return

    print("\nYour Tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

# Add a task
def add_task(tasks):
    task = input("Enter a new task: ").strip()
    if task:
        tasks.append(task)
        save_tasks(tasks)
        print("Task added.")
    else:
        print("Task cannot be empty.")

# Main program loop
def main():
    tasks = load_tasks()

    while True:
        print("\n--- Task Tracker ---")
        print("1. Add task")
        print("2. View tasks")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

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
        status = "✓" if task["completed"] else " "
        print(f"{i}. [{status}] {task['text']}")

# Add a task
def add_task(tasks):
    text = input("Enter a task: ").strip()
    if text:
        tasks.append({"text": text, "completed": False})
        save_tasks(tasks)
        print("Task added.")

# Mark task as completed
def complete_task(tasks):
    show_tasks(tasks)
    try:
        num = int(input("Enter task number to complete: "))
        tasks[num - 1]["completed"] = True
        save_tasks(tasks)
        print("Task marked as completed.")
    except (ValueError, IndexError):
        print("Invalid selection.")

# Main menu loop
def main():
    tasks = load_tasks()

    while True:
        print("\n--- Task Tracker ---")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

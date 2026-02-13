import json
import os

FILENAME = "tasks.json"

# ---------------------------
# File Handling
# ---------------------------

def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=2)

# ---------------------------
# Display Functions
# ---------------------------

def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\nYour Tasks:")
    print("-" * 30)

    completed_count = 0

    for i, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else " "
        if task["completed"]:
            completed_count += 1
        print(f"{i}. [{status}] {task['text']}")

    print("-" * 30)
    print(f"Progress: {completed_count}/{len(tasks)} tasks completed")

# ---------------------------
# Core Features
# ---------------------------

def add_task(tasks):
    text = input("Enter a new task: ").strip()

    if not text:
        print("Task cannot be empty.")
        return

    # Prevent duplicates
    if text.lower() in [task["text"].lower() for task in tasks]:
        print("That task already exists.")
        return

    tasks.append({
        "text": text,
        "completed": False
    })

    save_tasks(tasks)
    print("Task added successfully.")

def toggle_task(tasks):
    if not tasks:
        print("No tasks to update.")
        return

    show_tasks(tasks)

    try:
        number = int(input("Enter task number to toggle completion: "))
        tasks[number - 1]["completed"] = not tasks[number - 1]["completed"]
        save_tasks(tasks)
        print("Task updated.")
    except (ValueError, IndexError):
        print("Invalid task number.")

def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return

    show_tasks(tasks)

    try:
        number = int(input("Enter task number to delete: "))
        removed = tasks.pop(number - 1)
        save_tasks(tasks)
        print(f"Deleted task: {removed['text']}")
    except (ValueError, IndexError):
        print("Invalid task number.")

# ---------------------------
# Main Program Loop
# ---------------------------

def main():
    tasks = load_tasks()

    while True:
        print("\n===== TASK TRACKER =====")
        print("1. Add task")
        print("2. View tasks")
        print("3. Toggle task completion")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option (1–5): ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            toggle_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1–5.")

if __name__ == "__main__":
    main()

import sqlite3
import datetime

def connect_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        deadline TEXT,
                        status TEXT CHECK(status IN ('pending', 'completed')) NOT NULL DEFAULT 'pending')''')
    conn.commit()
    return conn

def add_task(description, deadline):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, deadline) VALUES (?, ?)", (description, deadline))
    conn.commit()
    conn.close()
    print("Task added successfully!")

def view_tasks(status=None,description=None):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    if status:
        query += " WHERE status = ?"
        cursor.execute(query, (status,))
    
    elif description:
        query += " WHERE description = ?"
        cursor.execute(query, (description,))
    else:
        cursor.execute(query)
    
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        print(task)

def update_task(task_id, new_description=None, new_status=None):
    conn = connect_db()
    cursor = conn.cursor()
    if new_description:
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
    if new_status:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    print("Task updated successfully!")

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully!")

def main():
    while True:
        print("\nTask Management System")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Filter task by description")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            desc = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ")
            try:
                add_task(desc, deadline)
            except sqlite3.OperationalError:
                print("unable to open database file")
            except sqlite3.IntegrityError:
                print("Invalid input values")
        elif choice == '2':
            try:
                view_tasks()
            except sqlite3.OperationalError:
                print("unable to open database file")
            except sqlite3.IntegrityError:
                print("Invalid input values")
        elif choice == '3':
            try:
                view_tasks("pending")
            except sqlite3.OperationalError:
                print("unable to open database file")
            except sqlite3.IntegrityError:
                print("Invalid input values")
        elif choice == '4':
            try:
                view_tasks("completed")
            except sqlite3.OperationalError:
                print("unable to open database file")
            except sqlite3.IntegrityError:
                print("Invalid input values")
        elif choice == '5':
            task_id = int(input("Enter task ID: "))
            new_desc = input("Enter new description (or press Enter to skip): ")
            new_status = input("Enter new status (pending/completed or press Enter to skip): ")
            try:
                update_task(task_id, new_desc if new_desc else None, new_status if new_status else None)
            except sqlite3.OperationalError:
                print("unable to open database file")
            except sqlite3.IntegrityError:
                print("Invalid input values")
        elif choice == '6':
            try:
                task_id = int(input("Enter task ID: "))
                delete_task(task_id)
            except sqlite3.OperationalError:
                print("unable to open database file")
            except sqlite3.IntegrityError:
                print("Invalid input values")
        elif choice == '7':
            try:
                description = input("Enter Description :")
                view_tasks(None,description)
            except sqlite3.OperationalError:
                print("unable to open database")
            except sqlite3.IntegrityError:
                print("Invalid input values")
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":

    main()

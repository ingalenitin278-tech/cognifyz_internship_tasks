"""Task 3: Console CRUD app for tasks (in-memory list)."""


class Task:
    def __init__(self, task_id, title, description="", status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status

    def __str__(self):
        return f"[{self.task_id}] {self.title} | {self.status}\n      {self.description or '(no description)'}"


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def create(self, title, description=""):
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def read_all(self):
        return self.tasks

    def find(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def update(self, task_id, title=None, description=None, status=None):
        task = self.find(task_id)
        if not task:
            return False
        if title:
            task.title = title
        if description is not None and description != "":
            task.description = description
        if status:
            task.status = status
        return True

    def delete(self, task_id):
        task = self.find(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        return True


def ask_id(prompt="Task ID: "):
    text = input(prompt).strip()
    return int(text) if text.isdigit() else None


def menu():
    print("\n=== TASK MANAGER ===")
    print("1. Add task\n2. View tasks\n3. Update task\n4. Delete task\n5. Exit")
    return input("Choose: ").strip()


def main():
    manager = TaskManager()
    while True:
        choice = menu()
        if choice == "1":
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            task = manager.create(title, input("Description: ").strip())
            print(f"Task added with ID {task.task_id}.")
        elif choice == "2":
            tasks = manager.read_all()
            if not tasks:
                print("No tasks yet.")
            for t in tasks:
                print(t)
        elif choice == "3":
            tid = ask_id()
            if tid is None or not manager.find(tid):
                print("Task not found.")
                continue
            print("Leave blank to keep the current value.")
            title = input("New title: ").strip()
            desc = input("New description: ").strip()
            status = input("New status (Pending/In Progress/Done): ").strip()
            manager.update(tid, title, desc, status)
            print("Task updated.")
        elif choice == "4":
            tid = ask_id()
            print("Task deleted." if tid is not None and manager.delete(tid) else "Task not found.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

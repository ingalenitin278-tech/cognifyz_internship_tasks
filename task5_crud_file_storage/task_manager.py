"""Task 5: CRUD app with persistent storage in a text file (one JSON record per line)."""
import json
import os

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.txt")


class Task:
    def __init__(self, task_id, title, description="", status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status

    def to_line(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_line(line):
        d = json.loads(line)
        return Task(d["task_id"], d["title"], d.get("description", ""), d.get("status", "Pending"))

    def __str__(self):
        return f"[{self.task_id}] {self.title} | {self.status}\n      {self.description or '(no description)'}"


class TaskManager:
    def __init__(self, path=FILE_NAME):
        self.path = path
        self.tasks = []
        self.load()

    # ---------- File I/O ----------
    def load(self):
        self.tasks = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for number, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        self.tasks.append(Task.from_line(line))
                    except (json.JSONDecodeError, KeyError):
                        print(f"Warning: skipped corrupted line {number}.")
        except FileNotFoundError:
            pass  # first run, file will be created on save
        except PermissionError:
            print("Error: no permission to read the tasks file.")
        except OSError as e:
            print(f"Error reading file: {e}")

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                for t in self.tasks:
                    f.write(t.to_line() + "\n")
            return True
        except OSError as e:
            print(f"Error saving file: {e}")
            return False

    # ---------- CRUD ----------
    def next_id(self):
        return max((t.task_id for t in self.tasks), default=0) + 1

    def create(self, title, description=""):
        task = Task(self.next_id(), title, description)
        self.tasks.append(task)
        self.save()
        return task

    def find(self, task_id):
        return next((t for t in self.tasks if t.task_id == task_id), None)

    def update(self, task_id, title="", description="", status=""):
        task = self.find(task_id)
        if not task:
            return False
        task.title = title or task.title
        task.description = description or task.description
        task.status = status or task.status
        self.save()
        return True

    def delete(self, task_id):
        task = self.find(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        self.save()
        return True


def ask_id():
    text = input("Task ID: ").strip()
    return int(text) if text.isdigit() else None


def main():
    manager = TaskManager()
    print(f"Loaded {len(manager.tasks)} task(s) from {os.path.basename(FILE_NAME)}")
    while True:
        print("\n=== TASK MANAGER (saved to file) ===")
        print("1. Add task\n2. View tasks\n3. Update task\n4. Delete task\n5. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            t = manager.create(title, input("Description: ").strip())
            print(f"Task added with ID {t.task_id}.")
        elif choice == "2":
            if not manager.tasks:
                print("No tasks yet.")
            for t in manager.tasks:
                print(t)
        elif choice == "3":
            tid = ask_id()
            if tid is None or not manager.find(tid):
                print("Task not found.")
                continue
            print("Leave blank to keep the current value.")
            manager.update(tid, input("New title: ").strip(), input("New description: ").strip(),
                           input("New status (Pending/In Progress/Done): ").strip())
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

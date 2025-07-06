import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime, timedelta

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, description, due_date=None, priority="Medium"):
        task = {
            "description": description,
            "due_date": due_date,
            "completed": False,
            "priority": priority
        }
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, index, description=None, due_date=None, priority=None):
        if description is not None:
            self.tasks[index]["description"] = description
        if due_date is not None:
            self.tasks[index]["due_date"] = due_date
        if priority is not None:
            self.tasks[index]["priority"] = priority
        self.save_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()

    def mark_completed(self, index):
        self.tasks[index]["completed"] = True
        self.save_tasks()

    def get_tasks(self, filter_by=None):
        now = datetime.now()
        if filter_by == "completed":
            return [t for t in self.tasks if t["completed"]]
        elif filter_by == "pending":
            return [t for t in self.tasks if not t["completed"]]
        elif filter_by == "due_soon":
            due_soon = []
            for t in self.tasks:
                if t["due_date"]:
                    try:
                        due = datetime.strptime(t["due_date"], "%Y-%m-%d")
                        if 0 <= (due - now).days <= 3 and not t["completed"]:
                            due_soon.append(t)
                    except ValueError:
                        continue
            return due_soon
        else:
            return self.tasks

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.manager = TaskManager()
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self):
        # Top frame for add task
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Task:").grid(row=0, column=0)
        self.desc_entry = tk.Entry(top_frame, width=30)
        self.desc_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Due Date (YYYY-MM-DD):").grid(row=0, column=2)
        self.due_entry = tk.Entry(top_frame, width=12)
        self.due_entry.grid(row=0, column=3, padx=5)

        tk.Label(top_frame, text="Priority:").grid(row=0, column=4)
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(top_frame, textvariable=self.priority_var, values=["Low", "Medium", "High"], width=8, state="readonly")
        self.priority_menu.grid(row=0, column=5, padx=5)

        tk.Button(top_frame, text="Add Task", command=self.add_task).grid(row=0, column=6, padx=5)

        # Filter options
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="View:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="all")
        filters = [("All", "all"), ("Completed", "completed"), ("Pending", "pending"), ("Due Soon", "due_soon")]
        for text, val in filters:
            tk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=val, command=self.refresh_tasks).pack(side=tk.LEFT)

        # Task list
        self.tree = ttk.Treeview(self.root, columns=("Description", "Due Date", "Priority", "Status"), show="headings", selectmode="browse")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons for actions
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Mark Completed", command=self.mark_completed).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def add_task(self):
        desc = self.desc_entry.get().strip()
        due = self.due_entry.get().strip()
        priority = self.priority_var.get()
        if not desc:
            messagebox.showwarning("Input Error", "Task description cannot be empty.")
            return
        if due:
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Input Error", "Due date must be in YYYY-MM-DD format.")
                return
        self.manager.add_task(desc, due if due else None, priority)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.refresh_tasks()

    def refresh_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        filter_by = self.filter_var.get()
        tasks = self.manager.get_tasks(None if filter_by == "all" else filter_by)
        for idx, t in enumerate(tasks):
            status = "Completed" if t["completed"] else "Pending"
            self.tree.insert("", "end", iid=idx, values=(t["description"], t["due_date"] or "", t.get("priority", "Medium"), status))

    def get_selected_index(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Task", "Please select a task first.")
            return None
        idx = int(selected[0])
        filter_by = self.filter_var.get()
        tasks = self.manager.get_tasks(None if filter_by == "all" else filter_by)
        # Map filtered index to actual index in self.manager.tasks
        if filter_by == "all":
            return idx
        else:
            task = tasks[idx]
            return self.manager.tasks.index(task)

    def mark_completed(self):
        idx = self.get_selected_index()
        if idx is not None:
            self.manager.mark_completed(idx)
            self.refresh_tasks()

    def edit_task(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        task = self.manager.tasks[idx]
        desc = simpledialog.askstring("Edit Description", "Edit task description:", initialvalue=task["description"])
        if desc is None or not desc.strip():
            return
        due = simpledialog.askstring("Edit Due Date", "Edit due date (YYYY-MM-DD):", initialvalue=task["due_date"] or "")
        if due:
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Input Error", "Due date must be in YYYY-MM-DD format.")
                return
        priority = simpledialog.askstring("Edit Priority", "Edit priority (Low, Medium, High):", initialvalue=task.get("priority", "Medium"))
        if priority not in ["Low", "Medium", "High"]:
            priority = "Medium"
        self.manager.edit_task(idx, desc.strip(), due if due else None, priority)
        self.refresh_tasks()

    def delete_task(self):
        idx = self.get_selected_index()
        if idx is not None:
            if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
                self.manager.delete_task(idx)
                self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox
import json
import os

# Task Class 
class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def toggle(self):
        self.completed = not self.completed

    def to_dict(self):
        return {"title": self.title, "completed": self.completed}

    @staticmethod
    def from_dict(d):
        return Task(d['title'], d['completed'])

# Task Manager Class 
class TaskManager:
    def __init__(self, file_path="tasks.json"):
        self.tasks = []
        self.file_path = file_path
        self.load()

    def add_task(self, title):
        if title.strip():
            self.tasks.append(Task(title))
            self.save()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save()

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].toggle()
            self.save()

    def clear_all(self):
        self.tasks = []
        self.save()

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(d) for d in data]
            except json.JSONDecodeError:
                self.tasks = []

    def get_tasks(self):
        return self.tasks

# Tkinter GUI 
class TodoApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("500x600")

        # Entry + Add Button
        self.entry = tk.Entry(root, width=25, font=("Arial", 14))
        self.entry.pack(pady=10)

        self.add_btn = tk.Button(root, text="Add Task", width=20, command=self.add_task)
        self.add_btn.pack(pady=5)

        # Listbox for tasks
        self.listbox = tk.Listbox(root, width=40, height=20, font=("Arial", 12))
        self.listbox.pack(pady=10)
        self.refresh_tasks()

        # Buttons for actions
        self.complete_btn = tk.Button(root, text="Mark Completed", width=20, command=self.mark_completed)
        self.complete_btn.pack(pady=2)

        self.delete_btn = tk.Button(root, text="Delete Task", width=20, command=self.delete_task)
        self.delete_btn.pack(pady=2)

        self.clear_btn = tk.Button(root, text="Clear All", width=20, command=self.clear_all)
        self.clear_btn.pack(pady=2)

    # GUI Methods 
    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        for task in self.manager.get_tasks():
            status = "[Done]" if task.completed else "[ ]"
            self.listbox.insert(tk.END, f"{status} {task.title}")

    def add_task(self):
        title = self.entry.get()
        if not title.strip():
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        self.manager.add_task(title)
        self.entry.delete(0, tk.END)
        self.refresh_tasks()

    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No task selected!")
            return
        self.manager.delete_task(selected[0])
        self.refresh_tasks()

    def mark_completed(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No task selected!")
            return
        self.manager.mark_completed(selected[0])
        self.refresh_tasks()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
            self.manager.clear_all()
            self.refresh_tasks()

#Run App 
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

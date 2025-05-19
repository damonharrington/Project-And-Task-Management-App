#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Team Task Manager")

        self.tasks = []
        self.groups = {}

        self.setup_ui()

    def setup_ui(self):
        self.title_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.assigned_to_var = tk.StringVar()
        self.priority_var = tk.StringVar(value='Medium')
        self.deadline_var = tk.StringVar()

        tk.Label(self.root, text="Task Title:").pack()
        tk.Entry(self.root, textvariable=self.title_var).pack(fill='x')

        tk.Label(self.root, text="Description:").pack()
        tk.Entry(self.root, textvariable=self.description_var).pack(fill='x')

        tk.Label(self.root, text="Group:").pack()
        self.group_dropdown = ttk.Combobox(self.root, textvariable=self.group_var, values=list(self.groups.keys()))
        self.group_dropdown.pack()

        tk.Label(self.root, text="Assign To:").pack()
        self.assigned_to_dropdown = ttk.Combobox(self.root, textvariable=self.assigned_to_var, values=[])
        self.assigned_to_dropdown.pack()

        tk.Button(self.root, text="Add Group", command=self.add_group).pack()
        tk.Button(self.root, text="Add Person to Group", command=self.add_person_to_group).pack()
        tk.Button(self.root, text="Remove Person from Group", command=self.remove_person_from_group).pack()

        tk.Label(self.root, text="Priority:").pack()
        self.priority_dropdown = ttk.Combobox(self.root, textvariable=self.priority_var, values=['High', 'Medium', 'Low'])
        self.priority_dropdown.pack()

        tk.Label(self.root, text="Deadline (YYYY-MM-DD):").pack()
        tk.Entry(self.root, textvariable=self.deadline_var).pack(fill='x')

        tk.Button(self.root, text="Add Task", command=self.add_task).pack(pady=5)

        self.task_listbox = tk.Listbox(self.root, width=80)
        self.task_listbox.pack(pady=10)

        tk.Button(self.root, text="Delete Selected Task", command=self.delete_selected_task).pack(pady=2)
        tk.Button(self.root, text="Show Task Distribution", command=self.show_graph).pack(pady=5)

        self.group_dropdown.bind("<<ComboboxSelected>>", self.update_assigned_dropdown)

    def update_assigned_dropdown(self, event=None):
        group = self.group_var.get()
        if group in self.groups:
            self.assigned_to_dropdown['values'] = self.groups[group]
        else:
            self.assigned_to_dropdown['values'] = []

    def add_group(self):
        def save():
            group = group_var.get().strip()
            if group and group not in self.groups:
                self.groups[group] = []
                self.group_dropdown['values'] = list(self.groups.keys())
                popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Add Group")
        group_var = tk.StringVar()
        tk.Label(popup, text="Group Name:").pack()
        tk.Entry(popup, textvariable=group_var).pack()
        tk.Button(popup, text="Add", command=save).pack()

    def add_person_to_group(self):
        def save():
            person = person_var.get().strip()
            group = group_var.get().strip()
            if group in self.groups and person and person not in self.groups[group]:
                self.groups[group].append(person)
                if self.group_var.get() == group:
                    self.update_assigned_dropdown()
                popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Add Person to Group")
        person_var = tk.StringVar()
        group_var = tk.StringVar(value=self.group_var.get())
        tk.Label(popup, text="Person's name:").pack()
        tk.Entry(popup, textvariable=person_var).pack()
        tk.Label(popup, text="Group:").pack()
        ttk.Combobox(popup, textvariable=group_var, values=list(self.groups.keys())).pack()
        tk.Button(popup, text="Add", command=save).pack()

    def remove_person_from_group(self):
        def remove():
            person = person_var.get().strip()
            group = group_var.get().strip()
            if group in self.groups and person in self.groups[group]:
                confirm = messagebox.askyesno("Confirm", f"Remove '{person}' from group '{group}'?")
                if confirm:
                    self.groups[group].remove(person)
                    self.tasks = [t for t in self.tasks if t['assigned_to'] != person or t['group'] != group]
                    if self.group_var.get() == group:
                        self.update_assigned_dropdown()
                    self.display_tasks()
                    popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Remove Person from Group")
        person_var = tk.StringVar()
        group_var = tk.StringVar(value=self.group_var.get())
        tk.Label(popup, text="Person's name:").pack()
        tk.Entry(popup, textvariable=person_var).pack()
        tk.Label(popup, text="Group:").pack()
        ttk.Combobox(popup, textvariable=group_var, values=list(self.groups.keys())).pack()
        tk.Button(popup, text="Remove", command=remove).pack()

    def add_task(self):
        title = self.title_var.get().strip()
        description = self.description_var.get().strip()
        group = self.group_var.get().strip()
        assigned_to = self.assigned_to_var.get().strip()
        priority = self.priority_var.get().strip()
        deadline_str = self.deadline_var.get().strip()

        if not title or not group:
            messagebox.showwarning("Validation", "Task title and group are required.")
            return

        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d') if deadline_str else None
        except ValueError:
            messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        self.tasks.append({
            'title': title,
            'description': description,
            'group': group,
            'assigned_to': assigned_to,
            'priority': priority,
            'deadline': deadline
        })

        self.display_tasks()

        self.title_var.set('')
        self.description_var.set('')
        self.group_var.set('')
        self.assigned_to_var.set('')
        self.priority_var.set('Medium')
        self.deadline_var.set('')
        self.assigned_to_dropdown['values'] = []

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.tasks):
            task_str = f"[{idx+1}] Group: {task['group']} | Title: {task['title']} | Description: {task['description']} | Assigned: {task['assigned_to']} | Priority: {task['priority']} | Deadline: {task['deadline'].strftime('%Y-%m-%d') if task['deadline'] else 'None'}"
            self.task_listbox.insert(tk.END, task_str)

    def delete_selected_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a task to delete.")
            return
        index = selection[0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
        if confirm:
            del self.tasks[index]
            self.display_tasks()

    def show_graph(self):
        if not self.group_var.get():
            messagebox.showinfo("Info", "Please select a group to see task distribution.")
            return

        group = self.group_var.get()
        if group not in self.groups:
            messagebox.showerror("Error", "Group not found.")
            return

        members = self.groups[group]
        member_task_count = {member: 0 for member in members}
        for task in self.tasks:
            if task['group'] == group and task['assigned_to'] in member_task_count:
                member_task_count[task['assigned_to']] += 1

        fig, ax = plt.subplots()
        ax.bar(member_task_count.keys(), member_task_count.values(), color='skyblue')
        ax.set_title(f'Task Distribution in Group: {group}')
        ax.set_ylabel('Number of Tasks')

        graph_window = tk.Toplevel(self.root)
        graph_window.title("Task Distribution Graph")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()


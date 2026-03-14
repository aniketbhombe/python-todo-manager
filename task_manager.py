import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
import csv
from datetime import datetime

TASK_FILE = "tasks.json"

# Load tasks
if os.path.exists(TASK_FILE):
    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []


# ---------------- FUNCTIONS ---------------- #

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task():
    title = task_entry.get()
    priority = priority_var.get()
    due_date = due_date_entry.get()

    if title == "" or title == "Enter your task...":
        messagebox.showwarning("Warning", "Please enter a task")
        return

    if due_date and due_date != "YYYY-MM-DD":
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except:
            messagebox.showwarning("Warning", "Use date format YYYY-MM-DD")
            return

    tasks.append({
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "done": False
    })

    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)

    update_list()
    save_tasks()


def delete_task():
    selected = task_listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task")
        return

    index = selected[0]
    tasks.pop(index)

    update_list()
    save_tasks()


def mark_done():
    selected = task_listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task")
        return

    index = selected[0]
    tasks[index]["done"] = not tasks[index]["done"]

    update_list()
    save_tasks()


def update_list(filter_text=""):
    task_listbox.delete(0, tk.END)

    for task in tasks:

        if filter_text.lower() not in task["title"].lower():
            continue

        status = "✔️" if task["done"] else "❌"
        due = ""

        if task["due_date"]:
            due = f" | Due: {task['due_date']}"

        text = f"{status} [{task['priority']}] {task['title']}{due}"

        task_listbox.insert(tk.END, text)

        color = "green"

        if task["priority"] == "High":
            color = "red"
        elif task["priority"] == "Medium":
            color = "orange"

        task_listbox.itemconfig(tk.END, fg=color)


def search_task():
    query = search_entry.get()

    if query == "Search your task...":
        query = ""

    update_list(query)


def export_tasks():
    with open("tasks_export.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Title", "Priority", "Due Date", "Done"])

        for t in tasks:
            writer.writerow([
                t["title"],
                t["priority"],
                t["due_date"],
                t["done"]
            ])

    messagebox.showinfo("Export", "Tasks exported to tasks_export.csv")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("My To-Do Manager")
root.geometry("600x520")
root.config(bg="white")


# Title
title_label = tk.Label(
    root,
    text="My To-Do Manager",
    font=("Arial", 20, "bold"),
    bg="white"
)
title_label.pack(pady=10)


# Task Entry with placeholder
task_entry = tk.Entry(root, width=35, fg="grey")
task_entry.insert(0, "Enter your task...")
task_entry.pack(pady=5)


def clear_task_placeholder(event):
    if task_entry.get() == "Enter your task...":
        task_entry.delete(0, tk.END)
        task_entry.config(fg="black")


def add_task_placeholder(event):
    if task_entry.get() == "":
        task_entry.insert(0, "Enter your task...")
        task_entry.config(fg="grey")


task_entry.bind("<FocusIn>", clear_task_placeholder)
task_entry.bind("<FocusOut>", add_task_placeholder)


# Priority dropdown
priority_var = tk.StringVar()
priority_menu = ttk.Combobox(
    root,
    textvariable=priority_var,
    values=["High", "Medium", "Low"],
    width=15
)
priority_menu.current(1)
priority_menu.pack(pady=5)


# Due date entry
due_date_entry = tk.Entry(root, width=20)
due_date_entry.insert(0, "YYYY-MM-DD")
due_date_entry.pack(pady=5)


# Button style
btn_style = {
    "font": ("Arial", 11, "bold"),
    "width": 20,
    "bg": "#4CAF50",
    "fg": "white"
}

add_button = tk.Button(root, text="Add Task", command=add_task, **btn_style)
add_button.pack(pady=4)

done_button = tk.Button(root, text="Mark Done / Undo", command=mark_done, **btn_style)
done_button.pack(pady=4)

delete_button = tk.Button(root, text="Delete Task", command=delete_task, **btn_style)
delete_button.pack(pady=4)

export_button = tk.Button(root, text="Export CSV", command=export_tasks, **btn_style)
export_button.pack(pady=4)


# Search Entry with placeholder
search_entry = tk.Entry(root, width=35, fg="grey")
search_entry.insert(0, "Search your task...")
search_entry.pack(pady=10)


def clear_search_placeholder(event):
    if search_entry.get() == "Search your task...":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="black")


def add_search_placeholder(event):
    if search_entry.get() == "":
        search_entry.insert(0, "Search your task...")
        search_entry.config(fg="grey")


search_entry.bind("<FocusIn>", clear_search_placeholder)
search_entry.bind("<FocusOut>", add_search_placeholder)


search_button = tk.Button(root, text="Search Task", command=search_task, **btn_style)
search_button.pack(pady=4)


# Task list
task_listbox = tk.Listbox(root, width=70, height=12)
task_listbox.pack(pady=10)


update_list()

root.mainloop()
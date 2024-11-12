from tkinter import *
import tkinter as tk
from tkinter import messagebox
from win10toast import ToastNotifier 
import threading
import time
from datetime import datetime

toaster = ToastNotifier()
screen = Tk()
screen.geometry("500x700")
screen.configure(bg="#79A8A0")
screen.title("Team Shy")

task_list = []

def AddTask():
    task = Input_entry.get()
    if task:
        task_list.append({"task": task, "subtasks": [], "schedule": None})
        updateTaskList()
        Input_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def AddSubTask():
    selected_task = ViewList_listbox.curselection()
    if selected_task:
        taskIndex = selected_task[0] // 2 
        if 0 <= taskIndex < len(task_list):
            subtask = Input_entry.get()
            if subtask:
                task_list[taskIndex]["subtasks"].append({"subtask": subtask, "schedule": None})
                updateTaskList()
                Input_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Input Error", "Please enter a subtask.")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to add a subtask.")

def SetSchedule():
    selected_task = ViewList_listbox.curselection()
    schedule_input = Input_entry.get()  
    try:
        schedule = datetime.strptime(schedule_input, "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Datetime Format Error", "Please enter date and time in YYYY-MM-DD HH:MM format.")
        return

    if selected_task:
        selected_index = selected_task[0]
        if ViewList_listbox.get(selected_index).startswith("  "): 
            main_task_index = int(ViewList_listbox.get(selected_index - 1).split('.')[0])
            subtask_index = int(ViewList_listbox.get(selected_index).split('.')[1].split(" - ")[0])
            if 0 <= main_task_index < len(task_list) and 0 <= subtask_index < len(task_list[main_task_index]["subtasks"]):
                task_list[main_task_index]["subtasks"][subtask_index]["schedule"] = schedule
                subtask = task_list[main_task_index]["subtasks"][subtask_index]["subtask"]
                start_notification_thread(subtask, schedule)
        else:
            task_index = int(ViewList_listbox.get(selected_index).split('.')[0])
            if 0 <= task_index < len(task_list):
                task_list[task_index]["schedule"] = schedule
                task = task_list[task_index]["task"]
                start_notification_thread(task, schedule)
        updateTaskList()
    else:
        messagebox.showwarning("Selection Error", "Please select a task or subtask to set a schedule.")

def updateTaskList():
    ViewList_listbox.delete(0, tk.END)
    for index, task in enumerate(task_list):
        task_schedule_str = f" (Scheduled: {task['schedule']})" 
        ViewList_listbox.insert(tk.END, f"{index}. {task['task']}{task_schedule_str}")
        for subindex, subtask in enumerate(task["subtasks"]):
            subtask_schedule_str = f" (Scheduled: {subtask['schedule']})" 
            ViewList_listbox.insert(tk.END, f"  {index}.{subindex} - Subtask: {subtask['subtask']}{subtask_schedule_str}")

def Delete():
    selected_task = ViewList_listbox.curselection()
    if selected_task:
        selected_index = selected_task[0]
        if ViewList_listbox.get(selected_index).startswith("  "):  
            main_task_index = int(ViewList_listbox.get(selected_index - 1).split('.')[0])
            subtask_index = int(ViewList_listbox.get(selected_index).split('.')[1].split(" - ")[0])
            if 0 <= main_task_index < len(task_list) and 0 <= subtask_index < len(task_list[main_task_index]["subtasks"]):
                del_subtask = task_list[main_task_index]["subtasks"].pop(subtask_index)
                messagebox.showinfo("Subtask Removed", f"Subtask '{del_subtask['subtask']}' removed.")
        else:  
            task_index = int(ViewList_listbox.get(selected_index).split('.')[0])
            if 0 <= task_index < len(task_list):
                del_task = task_list.pop(task_index)
                messagebox.showinfo("Task Removed", f"Task '{del_task['task']}' removed.")
        updateTaskList()
    else:
        messagebox.showwarning("Selection Error", "Please select a task or subtask to remove.")
        

def MarkAsDone():
    selected_task = ViewList_listbox.curselection()
    if selected_task:
        selected_index = selected_task[0]
        if ViewList_listbox.get(selected_index).startswith("  "): 
            main_task_index = int(ViewList_listbox.get(selected_index - 1).split('.')[0])
            subtask_index = int(ViewList_listbox.get(selected_index).split('.')[1].split(" - ")[0])
            if 0 <= main_task_index < len(task_list) and 0 <= subtask_index < len(task_list[main_task_index]["subtasks"]):
                del_subtask = task_list[main_task_index]["subtasks"].pop(subtask_index)
                messagebox.showinfo("Subtask", f"Subtask '{del_subtask['subtask']}' Finish.")
        else:  
            task_index = int(ViewList_listbox.get(selected_index).split('.')[0])
            if 0 <= task_index < len(task_list):
                del_task = task_list.pop(task_index)
                messagebox.showinfo("Task", f"Task '{del_task['task']}' Finish.")
        updateTaskList()
    else:
        messagebox.showwarning("Selection Error", "Please select a task or subtask to mark as done.")

def notification_check(task_name, schedule):
    while True:
        current_time = datetime.now()
        if current_time >= schedule:
            toaster.show_toast("Task Reminder", f"Task Due: {task_name} for {schedule}", duration=10, threaded=True)
            break
        time.sleep(30)

def start_notification_thread(task_name, schedule):
    thread = threading.Thread(target=notification_check, args=(task_name, schedule))
    thread.daemon = True
    thread.start()


Image_icon = PhotoImage(file="Image/taskk.png")
screen.iconphoto(False, Image_icon)

Menu_label = Label(screen, text="Task Wise", font=("times new roman", 40, "bold"), fg="Black", bg="#B4CDB3", border=15, width=100)
Menu_label.pack()

Add_label = tk.Label(screen, text="Enter your Task/SubTask", font=("times new roman", 20, "bold"), fg="white", bg="#79A8A0")
Add_label.pack(pady=(10, 0))

Add1_label = tk.Label(screen, text="Set Schedule(YYYY-MM-DD HH:MM)", font=("times new roman", 20, "bold"), fg="white", bg="#79A8A0")
Add1_label.pack(pady=(10, 0))

Input_entry = tk.Entry(screen, width=25, border=5, font=('Halvetica', 26))
Input_entry.pack(pady=(10))

Button_label = tk.Button(screen, text="Add Task", font=('Halvetica', 15), fg="black", bd=5, command=AddTask)
Button_label.place(x=10, y=260)

subButton_label = tk.Button(screen, text="Add SubTask", font=('Halvetica', 15), fg="black", bd=5, command=AddSubTask)
subButton_label.place(x=165, y=260)

scheduleButton_label = tk.Button(screen, text="Set Schedule", font=('Halvetica', 15), fg="black", bd=5, command=SetSchedule)
scheduleButton_label.place(x=350, y=260)

ViewList_listbox = tk.Listbox(screen, width=90, height=15, border=10)
ViewList_listbox.pack(pady=(99))

DeleteTask_button = tk.Button(screen, text="Delete Task", font=("Halvetica", 15), fg="black", bd=5, command=Delete)
DeleteTask_button.place(x=10, y=620)

MarkAsDone1_button = tk.Button(screen, text="Mark As Done", font=("Halvetica", 15), fg="black", bd=5, command=MarkAsDone)
MarkAsDone1_button.place(x=165, y=620)

screen.mainloop()

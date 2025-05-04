# please build this app below this comment: create a task app 

import tkinter as tk
from tkinter import ttk

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task App")
        self.root.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the task list
        self.task_frame = ttk.Frame(self.root, padding="10")
        self.task_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.task_frame.columnconfigure(0, weight=1)
        self.task_frame.rowconfigure(0, weight=1)

        # Create a listbox to display tasks
        self.task_listbox = tk.Listbox(self.task_frame, selectmode=tk.SINGLE, width=30, height=10)
        self.task_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Create a scrollbar for the listbox
        self.scrollbar = ttk.Scrollbar(self.task_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details



        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the ta
        # sk details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details
        # sk details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details

        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        # Create a frame for the task details
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")










    
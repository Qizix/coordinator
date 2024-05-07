import queue
from random import randint
import tkinter as tk
from tkinter import ttk
import numpy as np
import os
 
class QueueVisualization:
    def __init__(self, master, filename):
        self.master = master
        self.filename = filename
        self.tree = ttk.Treeview(master, columns=("current_states", "desired_states", "input_x", "previous_setpoints", "environment_state",), show="headings")
        self.tree.heading("current_states", text="current_states")
        self.tree.heading("desired_states", text="desired_states")
        self.tree.heading("input_x", text="input_x")
        self.tree.heading("previous_setpoints", text="previous_setpoints")
        self.tree.heading("environment_state", text="environment_state")
        self.tree.pack()

        self.last_modified_time = os.path.getmtime(filename)
        self.load_queue_and_display()
        self.check_file_changes()

    def load_queue_and_display(self):
        with open(self.filename, 'rb') as f:
            data_list = np.load(f, allow_pickle=True)

            for item in self.tree.get_children():
              self.tree.delete(item)

            for idx, data in enumerate(data_list):
                num_parts = int(data[-2])
                current_states = data[:num_parts]
                desired_states = data[num_parts : 2*num_parts]
                input_x = data[2*num_parts : 3*num_parts]
                previous_setpoints = data[3*num_parts : 4*num_parts]
                environment_state = data[-1]

                self.tree.insert("", "end", text=str(idx+1), values=(current_states, desired_states, input_x, previous_setpoints, environment_state))

    def check_file_changes(self):
        current_modified_time = os.path.getmtime(self.filename) 
        if current_modified_time != self.last_modified_time:

            self.last_modified_time = current_modified_time
            self.load_queue_and_display()


        self.master.after(1000, self.check_file_changes)





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Queue Visualization")
    visualization = QueueVisualization(root, 'data_queue.npy')
    root.mainloop()
    print("qqqqqqqqqqq")

    

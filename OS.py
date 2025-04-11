import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import random


class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2f")

        self.frames = 3
        self.pages = [random.randint(1, 5) for _ in range(10)]
        self.current_frame = 0
        self.history = []
        self.page_fault_indices = []
        self.page_faults = 0

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#1e1e2f")
        style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 12))
        style.configure("TButton", background="#5e60ce", foreground="white", font=("Segoe UI", 11), padding=8)
        style.map("TButton", background=[("active", "#7b7efb")])
        style.configure("TCombobox", font=("Segoe UI", 11), padding=4)
        style.map("TCombobox", fieldbackground=[("readonly", "#27293d")],
                   foreground=[("readonly", "white")])

    def build_ui(self):
        control_frame = ttk.Frame(self.root, padding=20)
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="Select Algorithm:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.algo_choice = ttk.Combobox(control_frame, values=["FIFO", "LRU", "Optimal"], state="readonly")
        self.algo_choice.set("FIFO")
        self.algo_choice.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(control_frame, text="Page References (comma-separated):").grid(
            row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.page_input = ttk.Entry(control_frame, width=30)
        self.page_input.insert(0, ",".join(map(str, self.pages)))
        self.page_input.grid(row=1, column=1, padx=10, pady=5)

        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.run_button = ttk.Button(btn_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(btn_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.page_fault_label = ttk.Label(control_frame, text="Page Faults: 0")
        self.page_fault_label.grid(row=3, column=0, columnspan=2)

        graph_frame = ttk.Frame(self.root)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.fig, self.ax = plt.subplots(facecolor='#1e1e2f')
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=5)

        self.prev_btn = ttk.Button(nav_frame, text="Previous", command=self.prev_frame)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(nav_frame, text="Next", command=self.next_frame)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.step_info = ttk.Label(nav_frame, text="Step: 0 / 0")
        self.step_info.pack(side=tk.LEFT, padx=10)

    def fifo_algorithm(self):
        queue = []
        page_faults = 0
        history = []
        fault_indices = []

        for i, page in enumerate(self.pages):
            if page not in queue:
                if len(queue) < self.frames:
                    queue.append(page)
                else:
                    queue.pop(0)
                    queue.append(page)
                page_faults += 1
                fault_indices.append(i)
            history.append(queue.copy())

        self.page_fault_indices = fault_indices
        return history, page_faults

    def lru_algorithm(self):
        queue = []
        recent = {}
        page_faults = 0
        history = []
        fault_indices = []

        for i, page in enumerate(self.pages):
            if page in queue:
                recent[page] = i
            else:
                if len(queue) < self.frames:
                    queue.append(page)
                else:
                    lru_page = min(queue, key=lambda x: recent.get(x, -1))
                    queue[queue.index(lru_page)] = page
                recent[page] = i
                page_faults += 1
                fault_indices.append(i)
            history.append(queue.copy())

        self.page_fault_indices = fault_indices
        return history, page_faults

    def optimal_algorithm(self):
        queue = []
        page_faults = 0
        history = []
        fault_indices = []

        for i in range(len(self.pages)):
            page = self.pages[i]
            if page not in queue:
                if len(queue) < self.frames:
                    queue.append(page)
                else:
                    future = self.pages[i+1:]
                    indices = [(future.index(p) if p in future else float('inf')) for p in queue]
                    farthest = indices.index(max(indices))
                    queue[farthest] = page
                page_faults += 1
                fault_indices.append(i)
            history.append(queue.copy())

        self.page_fault_indices = fault_indices
        return history, page_faults

    def run_simulation(self):
        algo = self.algo_choice.get()
        try:
            self.pages = list(map(int, self.page_input.get().strip().split(',')))
        except:
            messagebox.showerror("Invalid Input", "Please enter valid comma-separated numbers.")
            return

        self.current_frame = 0
        self.run_button.state(["disabled"])

        if algo == "FIFO":
            self.history, self.page_faults = self.fifo_algorithm()
        elif algo == "LRU":
            self.history, self.page_faults = self.lru_algorithm()
        elif algo == "Optimal":
            self.history, self.page_faults = self.optimal_algorithm()
        else:
            return

        self.page_fault_label.config(text=f"Page Faults: {self.page_faults}")
        self.update_frame_display()

    def update_frame_display(self):
        self.ax.clear()
        self.ax.set_facecolor('#1e1e2f')
        self.ax.set_title(f"{self.algo_choice.get()} Algorithm", fontsize=14, color='white')
        self.ax.set_xlabel("Frame Slot", color="white")
        self.ax.set_ylabel("Page Number", color="white")
        self.ax.tick_params(colors='white')

        if self.current_frame < len(self.history):
            frame = self.history[self.current_frame]
            if self.current_frame in self.page_fault_indices:
                colors = ['red'] * len(frame)
            else:
                colors = ['#5e60ce'] * len(frame)
            self.ax.bar(range(len(frame)), frame, color=colors)
            self.ax.set_ylim(0, max(self.pages) + 1)

        self.step_info.config(text=f"Step: {self.current_frame + 1} / {len(self.history)}")
        self.canvas.draw()
        self.run_button.state(["!disabled"])

    def next_frame(self):
        if self.current_frame < len(self.history) - 1:
            self.current_frame += 1
            self.update_frame_display()

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.update_frame_display()

    def reset_simulation(self):
        self.history = []
        self.current_frame = 0
        self.page_fault_indices = []
        self.page_fault_label.config(text="Page Faults: 0")
        self.step_info.config(text="Step: 0 / 0")
        self.ax.clear()
        self.canvas.draw()
        self.run_button.state(["!disabled"])


if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()

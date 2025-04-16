import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithm Simulator")
        self.root.geometry("800x600")

        self.algorithm = tk.StringVar(value="FIFO")
        self.frames = 3
        self.page_sequence = []
        self.history = []

        self.setup_ui()

    def setup_ui(self):
        # Control Frame
        control_frame = ttk.LabelFrame(self.root, text="Controls")
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Algorithm Selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        algo_menu = ttk.Combobox(control_frame, textvariable=self.algorithm, values=["FIFO", "LRU", "Optimal"], state="readonly")
        algo_menu.grid(row=0, column=1, padx=5, pady=5)

        # Number of Frames
        ttk.Label(control_frame, text="Number of Frames:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.frame_input = ttk.Entry(control_frame, width=10)
        self.frame_input.insert(0, str(self.frames))
        self.frame_input.grid(row=1, column=1, padx=5, pady=5)

        # Page Sequence
        ttk.Label(control_frame, text="Page Sequence (space-separated):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.sequence_input = ttk.Entry(control_frame, width=50)
        self.sequence_input.grid(row=2, column=1, padx=5, pady=5)

        # Run Button
        run_button = ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
        run_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Output Frame
        output_frame = ttk.LabelFrame(self.root, text="Simulation Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=output_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Step Explanation
        self.step_explanation = ttk.Label(self.root, text="", font=("Segoe UI", 10))
        self.step_explanation.pack(pady=5)

    def run_simulation(self):
        # Clear previous output
        self.ax.clear()
        self.step_explanation.config(text="")
        self.history.clear()

        # Get user inputs
        try:
            self.frames = int(self.frame_input.get())
            if self.frames <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of frames must be a positive integer.")
            return

        sequence_str = self.sequence_input.get().strip()
        if not sequence_str:
            messagebox.showerror("Invalid Input", "Please enter a page sequence.")
            return

        try:
            self.page_sequence = list(map(int, sequence_str.split()))
        except ValueError:
            messagebox.showerror("Invalid Input", "Page sequence must contain integers separated by spaces.")
            return

        # Run selected algorithm
        algo = self.algorithm.get()
        if algo == "FIFO":
            self.simulate_fifo()
        elif algo == "LRU":
            self.simulate_lru()
        elif algo == "Optimal":
            self.simulate_optimal()
        else:
            messagebox.showerror("Invalid Algorithm", f"Algorithm '{algo}' is not supported.")
            return

        # Display results
        self.display_results()

    def simulate_fifo(self):
        frame = []
        page_faults = 0
        for page in self.page_sequence:
            if page not in frame:
                if len(frame) < self.frames:
                    frame.append(page)
                else:
                    frame.pop(0)
                    frame.append(page)
                page_faults += 1
            self.history.append(list(frame))
        self.step_explanation.config(text=f"FIFO Algorithm: {page_faults} page faults.")

    def simulate_lru(self):
        frame = []
        recent_usage = []
        page_faults = 0
        for page in self.page_sequence:
            if page in frame:
                recent_usage.remove(page)
                recent_usage.append(page)
            else:
                if len(frame) < self.frames:
                    frame.append(page)
                else:
                    lru_page = recent_usage.pop(0)
                    frame[frame.index(lru_page)] = page
                recent_usage.append(page)
                page_faults += 1
            self.history.append(list(frame))
        self.step_explanation.config(text=f"LRU Algorithm: {page_faults} page faults.")

    def simulate_optimal(self):
        frame = []
        page_faults = 0
        for i in range(len(self.page_sequence)):
            page = self.page_sequence[i]
            if page not in frame:
                if len(frame) < self.frames:
                    frame.append(page)
                else:
                    future_uses = []
                    for f_page in frame:
                        if f_page in self.page_sequence[i+1:]:
                            future_uses.append(self.page_sequence[i+1:].index(f_page))
                        else:
                            future_uses.append(float('inf'))
                    victim_index = future_uses.index(max(future_uses))
                    frame[victim_index] = page
                page_faults += 1
            self.history.append(list(frame))
        self.step_explanation.config(text=f"Optimal Algorithm: {page_faults} page faults.")

    def display_results(self):
        self.ax.set_title("Page Replacement Simulation")
        self.ax.set_xlabel("Step")
        self.ax.set_ylabel("Frame Content")

        for step, frame in enumerate(self.history):
            for idx, val in enumerate(frame):
                self.ax.text(step, self.frames - idx - 1, str(val), ha='center', va='center', bbox=dict(facecolor='skyblue', edgecolor='black'))

        self.ax.set_xticks(range(len(self.history)))
        self.ax.set_yticks(range(self.frames))
        self.ax.set_yticklabels([f"Frame {i+1}" for i in range(self.frames)][::-1])
        self.ax.set_xlim(-1, len(self.history))
        self.ax.set_ylim(-1, self.frames)
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()

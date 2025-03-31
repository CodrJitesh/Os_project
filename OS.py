import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class BankersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm Visualizer")
        self.style = ttk.Style()
        self.configure_styles()
        self.create_widgets()
        self.test_cases = self.get_test_cases()
        # self.canvas.scale("all", 0, 0, 1.5, 1.5)
        self.root.state('zoomed')
        # root = tk.Tk()
        root.tk.call('tk', 'scaling', 2.0)
        # self.canvas = tk.Canvas(self.root, bg="white", width=1000, height=600)  # Set desired size
        # self.canvas.pack(side="right", padx=10, pady=10)
        # canvas = tk.Canvas(root)
        # canvas.scale("all", 0, 0, 1.5, 1.5)
        
    def configure_styles(self):
        self.style.theme_create("bankers", parent="alt", settings={
            "TFrame": {"configure": {"background": "#2E2E2E"}},
            "TLabel": {"configure": {
                "background": "#2E2E2E",
                "foreground": "#FFFFFF",
                "font": ("Segoe UI", 10)
            }},
            "TButton": {"configure": {
                "font": ("Segoe UI", 10, "bold"),
                "borderwidth": 1,
                "relief": "flat",
                "padding": 5
            }, "map": {
                "background": [("active", "#4A4A4A"), ("pressed", "#3A3A3A")],
                "foreground": [("active", "white")]
            }},
            "TCombobox": {"configure": {
                "fieldbackground": "#404040",
                "background": "#404040",
                "arrowcolor": "white"
            }},
            "TEntry": {"configure": {
                "fieldbackground": "#404040",
                "foreground": "white"
            }},
            "TNotebook": {"configure": {
                "background": "#2E2E2E",
                "borderwidth": 0
            }},
            "TNotebook.Tab": {
                "configure": {
                    "padding": [10, 5],
                    "background": "#404040",
                    "foreground": "white",
                    "font": ("Segoe UI", 9, "bold")
                },
                "map": {
                    "background": [("selected", "#505050")],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            }
        })
        self.style.theme_use("bankers")

    def create_widgets(self):
        self.root.configure(background="#2E2E2E")
        self.root.geometry("1200x800")
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel
        left_panel = ttk.Frame(main_frame, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # Right panel
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ----------------- Left Panel Contents -----------------
        # Test case section
        test_case_frame = ttk.LabelFrame(left_panel, text=" Test Cases ", padding=10)
        test_case_frame.pack(fill=tk.X, pady=5)
        
        self.test_case_var = tk.StringVar()
        self.test_case_combobox = ttk.Combobox(test_case_frame, textvariable=self.test_case_var, 
                                              values=[f"Test Case {i}" for i in range(1, 9)])
        self.test_case_combobox.pack(fill=tk.X, pady=3)
        ttk.Button(test_case_frame, text="Load Selected Case", command=self.load_test_case, 
                  style="Accent.TButton").pack(fill=tk.X, pady=5)
        
        # System parameters
        param_frame = ttk.LabelFrame(left_panel, text=" System Parameters ", padding=10)
        param_frame.pack(fill=tk.X, pady=5)
        
        input_grid = ttk.Frame(param_frame)
        input_grid.pack(fill=tk.X)
        
        ttk.Label(input_grid, text="Processes:").grid(row=0, column=0, sticky=tk.W)
        self.n_entry = ttk.Entry(input_grid, width=8)
        self.n_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_grid, text="Resources:").grid(row=1, column=0, sticky=tk.W)
        self.m_entry = ttk.Entry(input_grid, width=8)
        self.m_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_grid, text="Total Resources:").grid(row=2, column=0, sticky=tk.W)
        self.total_resources_entry = ttk.Entry(input_grid)
        self.total_resources_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.EW)
        
        # Matrices notebook
        matrix_notebook = ttk.Notebook(left_panel)
        matrix_notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Allocation tab
        alloc_frame = ttk.Frame(matrix_notebook)
        self.allocation_text = scrolledtext.ScrolledText(alloc_frame, bg="#404040", fg="white",
                                                        insertbackground="white", wrap=tk.NONE)
        self.allocation_text.pack(fill=tk.BOTH, expand=True)
        matrix_notebook.add(alloc_frame, text="Allocation Matrix")
        
        # Maximum tab
        max_frame = ttk.Frame(matrix_notebook)
        self.maximum_text = scrolledtext.ScrolledText(max_frame, bg="#404040", fg="white",
                                                     insertbackground="white", wrap=tk.NONE)
        self.maximum_text.pack(fill=tk.BOTH, expand=True)
        matrix_notebook.add(max_frame, text="Maximum Matrix")
        
        # ----------------- Right Panel Contents -----------------
        # Visualization canvas
        canvas_frame = ttk.Frame(right_panel)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#808080", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = ttk.Frame(right_panel)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="⟳ Run Analysis", command=self.run_algorithm,
                  style="Accent.TButton").pack(side=tk.RIGHT, padx=5)
        self.result_label = ttk.Label(control_frame, text="Ready", font=('Segoe UI', 11, 'bold'),
                                     foreground="#888888")
        self.result_label.pack(side=tk.LEFT)
        
        # Add modern scrollbars to canvas
        self.x_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.x_scroll.pack(fill=tk.X)
        self.y_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
        
        # Create custom style for accent button
        self.style.configure("Accent.TButton", background="#4CAF50", foreground="white",
                            font=('Segoe UI', 15, 'bold'))

    def load_test_case(self):
        case_number = int(self.test_case_combobox.get().split()[-1])
        test_case = self.test_cases[case_number]
        
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, str(test_case['n']))
        
        self.m_entry.delete(0, tk.END)
        self.m_entry.insert(0, str(test_case['m']))
        
        self.total_resources_entry.delete(0, tk.END)
        self.total_resources_entry.insert(0, " ".join(map(str, test_case['total_resources'])))
        
        self.allocation_text.delete(1.0, tk.END)
        self.allocation_text.insert(tk.END, "\n".join([" ".join(map(str, row)) for row in test_case['allocation']]))
        
        self.maximum_text.delete(1.0, tk.END)
        self.maximum_text.insert(tk.END, "\n".join([" ".join(map(str, row)) for row in test_case['maximum']]))

    def get_test_cases(self):
        # Same test case data as before
        return {
            1: {
            'n': 5,
            'm': 3,
            'total_resources': [10, 5, 7],
            'allocation': [
                [0, 1, 0],
                [2, 0, 0],
                [3, 0, 2],
                [2, 1, 1],
                [0, 0, 2]
            ],
            'maximum': [
                [7, 5, 3],
                [3, 2, 2],
                [9, 0, 2],
                [2, 2, 2],
                [4, 3, 3]
            ]
        },
        2: {
            'n': 3,
            'm': 3,
            'total_resources': [10, 5, 7],
            'allocation': [
                [0, 1, 0],
                [2, 0, 0],
                [3, 0, 2]
            ],
            'maximum': [
                [7, 5, 3],
                [3, 2, 2],
                [9, 0, 2]
            ]
        },
        3: {
            'n': 4,
            'm': 2,
            'total_resources': [8, 6],
            'allocation': [
                [1, 1],
                [2, 1],
                [1, 2],
                [1, 1]
            ],
            'maximum': [
                [3, 3],
                [4, 3],
                [3, 2],
                [2, 2]
            ]
        },
        4: {
            'n': 4,
            'm': 2,
            'total_resources': [5, 5],
            'allocation': [
                [2, 1],
                [1, 2],
                [1, 1],
                [0, 0]
            ],
            'maximum': [
                [4, 3],
                [3, 4],
                [2, 2],
                [4, 3]
            ]
            
        },
        5: {
            'n': 3,
            'm': 3,
            'total_resources': [7, 7, 7],
            'allocation': [
                [3, 3, 3],
                [2, 2, 2],
                [1, 1, 1]
            ],
            'maximum': [
                [7, 7, 7],
                [6, 6, 6],
                [5, 5, 5]
            ]
        },
        6: {
            'n': 3,
            'm': 3,
            'total_resources': [6, 6, 6],
            'allocation': [
                [2, 2, 1],
                [1, 1, 3],
                [2, 1, 1]
            ],
            'maximum': [
                [4, 4, 2],
                [5, 4, 4],
                [3, 3, 3]
            ]
        },
        7: {
            'n': 4,
            'm': 2,
            'total_resources': [10, 10],
            'allocation': [
                [3, 3],
                [2, 2],
                [3, 2],
                [1, 2]
            ],
            'maximum': [
                [8, 7],
                [5, 6],
                [7, 4],
                [4, 5]
            ]
        },
        8: {
            'n': 3,
            'm': 3,
            'total_resources': [5, 5, 5],
            'allocation': [
                [1, 2, 1],
                [2, 1, 2],
                [1, 1, 1]
            ],
            'maximum': [
                [3, 3, 3],
                [3, 3, 3],
                [3, 3, 3]
            ]
        }
        }

    def run_algorithm(self):
        try:
            # Collect input data
            n = int(self.n_entry.get())
            m = int(self.m_entry.get())
            total_resources = list(map(int, self.total_resources_entry.get().split()))
            
            # Validate matrix dimensions
            allocation = []
            allocation_lines = self.allocation_text.get(1.0, tk.END).splitlines()
            for i, line in enumerate(allocation_lines):
                if line.strip():
                    row = list(map(int, line.split()))
                    if len(row) != m:
                        raise ValueError(f"Allocation matrix row {i} has {len(row)} entries, expected {m}")
                    allocation.append(row)
            if len(allocation) != n:
                raise ValueError(f"Allocation matrix has {len(allocation)} rows, expected {n}")
            
            maximum = []
            maximum_lines = self.maximum_text.get(1.0, tk.END).splitlines()
            for i, line in enumerate(maximum_lines):
                if line.strip():
                    row = list(map(int, line.split()))
                    if len(row) != m:
                        raise ValueError(f"Maximum matrix row {i} has {len(row)} entries, expected {m}")
                    maximum.append(row)
            if len(maximum) != n:
                raise ValueError(f"Maximum matrix has {len(maximum)} rows, expected {n}")
            
            # Calculate allocated and available resources
            allocated = [sum(allocation[i][j] for i in range(n)) for j in range(m)]
            available = [total_resources[j] - allocated[j] for j in range(m)]
            
            # Calculate need matrix
            need = []
            for i in range(n):
                row = [maximum[i][j] - allocation[i][j] for j in range(m)]
                need.append(row)
            
            # Initialize work and finish arrays
            work = available.copy()
            finish = [False] * n
            safe_sequence = []
            
            # Check for resource starvation
            total_available = [available[j] + sum(allocation[i][j] for i in range(n)) for j in range(m)]
            for i in range(n):
                if any(maximum[i][j] > total_available[j] for j in range(m)):
                    self.display_results(False, [])
                    self.draw_rag(n, m, allocation, maximum, available, need)
                    messagebox.showwarning("Resource Starvation", 
                                        f"Process P{i} requests more resources than exist in the system")
                    return
            
            # Run Banker's algorithm
            attempts = 0
            max_attempts = n * 2  # Allow multiple passes through process list
            
            while False in finish and attempts < max_attempts:
                found = False
                for i in range(n):
                    if not finish[i]:
                        # Check if process can complete with current resources
                        can_complete = all(need[i][j] <= work[j] for j in range(m))
                        
                        if can_complete:
                            # Process can run, add its resources back
                            for j in range(m):
                                work[j] += allocation[i][j]
                            finish[i] = True
                            safe_sequence.append(f"P{i}")
                            found = True
                            break
                
                if not found:
                    attempts += 1
                    if attempts >= max_attempts:
                        break  # Deadlock detected
            
            # Check if all processes finished
            is_safe = all(finish)
            
            # Display results
            self.display_results(is_safe, safe_sequence)
            self.draw_rag(n, m, allocation, maximum, available, need)
            
            # Show detailed explanation
            explanation = self.generate_explanation(is_safe, safe_sequence, n, finish, allocation, need, available)
            self.show_explanation(explanation)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def generate_explanation(self, is_safe, sequence, n, finish, allocation, need, available):
        explanation = []
        
        if is_safe:
            explanation.append("SYSTEM IS IN A SAFE STATE")
            explanation.append("\nSafe execution sequence:")
            explanation.append(" → ".join(sequence))
            
            explanation.append("\n\nStep-by-step explanation:")
            work = available.copy()
            for i, process in enumerate(sequence):
                pid = int(process[1:])  # Extract process number from "P0", "P1", etc.
                explanation.append(f"\nStep {i+1}: Execute {process}")
                explanation.append(f"- Currently holds: {allocation[pid]}")
                explanation.append(f"- Needs: {need[pid]}")
                explanation.append(f"- Work available: {work}")
                
                # Show resources being released
                new_work = [work[j] + allocation[pid][j] for j in range(len(work))]
                explanation.append(f"- After completion, releases resources: {allocation[pid]}")
                explanation.append(f"- New work available: {new_work}")
                work = new_work
        else:
            explanation.append("SYSTEM IS IN AN UNSAFE STATE - DEADLOCK DETECTED")
            
            blocked = [i for i in range(n) if not finish[i]]
            explanation.append(f"\nBlocked processes: {', '.join(f'P{i}' for i in blocked)}")
            
            explanation.append("\nDeadlock analysis:")
            for i in blocked:
                explanation.append(f"\nProcess P{i}:")
                explanation.append(f"- Currently holds: {allocation[i]}")
                explanation.append(f"- Needs: {need[i]}")
                explanation.append(f"- Available resources: {available}")
                
                # Find which resources are insufficient
                insufficient = [j for j in range(len(available)) if need[i][j] > available[j]]
                if insufficient:
                    explanation.append(f"- Cannot proceed because resources {insufficient} are insufficient")
                else:
                    explanation.append("- Could theoretically run (this suggests a circular wait)")
        
        return "\n".join(explanation)

    def show_explanation(self, text):
        # Create a new window for detailed explanation
        win = tk.Toplevel(self.root)
        win.title("Detailed Explanation")
        
        text_widget = scrolledtext.ScrolledText(win, width=80, height=25, wrap=tk.WORD)
        text_widget.insert(tk.END, text)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def display_results(self, safe, sequence):
        text = "SAFE STATE - Sequence: " + " → ".join(sequence) if safe else "UNSAFE STATE - Deadlock Detected"
        color = "green" if safe else "red"
        self.result_label.config(text=text, foreground=color)

    def draw_rag(self, n, m, allocation, maximum, available, need):
        self.canvas.delete("all")
        node_size = 80
        spacing = 200
        canvas_width = max(800, m * 150 + 400)
        self.canvas.config(scrollregion=(0, 0, canvas_width, n * spacing + 100))

        process_nodes = {}
        resource_nodes = {}

        # Draw processes (left side)
        for i in range(n):
            x, y = 200, 150 + i * spacing
            self.canvas.create_oval(x, y, x + node_size, y + node_size,
                                    fill="#2196F3", outline="#1976D2", width=2)
            self.canvas.create_text(x + node_size / 2, y + node_size / 2,
                                    text=f"P{i}", fill="white",
                                    font=('Segoe UI', 10, 'bold'))
            process_nodes[i] = (x + node_size, y + node_size / 2)

        # Draw resources (right side)
        for j in range(m):
            x, y = 700, 150 + j * spacing 
            self.canvas.create_rectangle(x + 2, y + 2, x + node_size + 2, y + node_size + 2,
                                        fill="#666666", outline="")
            self.canvas.create_rectangle(x, y, x + node_size, y + node_size,
                                        fill="#607D8B", outline="#455A64", width=2)
            self.canvas.create_text(x + node_size / 2, y + node_size / 2,
                                    text=f"R{j}\n{available[j]}/{available[j] + sum(a[j] for a in allocation)}",
                                    fill="white", font=('Segoe UI', 9))
            resource_nodes[j] = (x, y + node_size / 2)

        # Draw allocation edges (solid green)
        for i in range(n):
            for j in range(m):
                if allocation[i][j] > 0:
                    self.create_curved_arrow(resource_nodes[j], process_nodes[i],
                                            allocation[i][j], "#1fff00", solid=True)

        # Draw request edges (dashed orange)
        for i in range(n):
            for j in range(m):
                if need[i][j] > 0:
                    self.create_curved_arrow(process_nodes[i], resource_nodes[j],
                                            need[i][j], "#FF5722", solid=False)

    def create_curved_arrow(self, start, end, quantity, color, solid=True):
        x1, y1 = start
        x2, y2 = end

        # Offset to prevent overlap
        offset = 20 if solid else -20  

        # Control point for Bezier curve
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 + offset

        # Draw curved edge
        self.canvas.create_line(x1, y1, cx, cy, x2, y2, fill=color, width=3,
                                arrow=tk.LAST, arrowshape=(0,0,0),
                                smooth=True, splinesteps=12,
                                dash=() if solid else (5, 3))  # Dashed for request edges
        # Find the midpoint of the edge
        if True:
            label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2

            # Compute perpendicular offset
            dx = x2 - x1
            dy = y2 - y1
            length = (dx**2 + dy**2) ** 0.5  # Distance between points

            if length != 0:
                dx /= length
                dy /= length

            # Apply perpendicular shift (adjust 15 pixels as needed)
            offset_x = dy * 25
            offset_y = -dx * 10

            # Adjust the label position
            label_x += offset_x
            label_y += offset_y

            # Draw the background rectangle
            # self.canvas.create_rectangle(label_x - 15, label_y - 10, label_x + 15, label_y + 10, outline="")

            # Draw the quantity text
            if solid:
                self.canvas.create_text(label_x, label_y, text=str(quantity), fill="white",
                                    font=('Segoe UI', 12, 'bold'))
            # else:
            #     self.canvas.create_text(label_x, label_y, text=str(quantity), fill="white",
            #                         font=('Segoe UI', 12, 'bold'))


if __name__ == "__main__":
    root = tk.Tk()
    app = BankersGUI(root)
    root.mainloop()
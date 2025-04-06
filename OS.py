import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import google.generativeai as genai
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
        try:
            # !! REPLACE "YOUR_API_KEY_HERE" WITH YOUR ACTUAL KEY !!
            self.api_key = "AIzaSyDKPfQibC8-8hpp0d5Wxq1SI_TUspteeno"
            if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
                 print("WARNING: API Key not set. AI feature will fail.")
                 self.ai_enabled = False
            else:
                genai.configure(api_key=self.api_key)
                self.ai_enabled = True
                print("Gemini AI Configured.") # Optional confirmation
        except Exception as e:
             print(f"ERROR: Failed to configure Gemini API: {e}")
             self.ai_enabled = False
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
            self.show_explanation(explanation, is_safe, safe_sequence, finish)
            
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

    def show_explanation(self, text, is_safe, safe_sequence, finish_list):
        # Create a new window for detailed explanation
        win = tk.Toplevel(self.root)
        win.title("Detailed Explanation")
        
        text_widget = scrolledtext.ScrolledText(win, width=80, height=25, wrap=tk.WORD)
        text_widget.insert(tk.END, text)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.config(state=tk.DISABLED) # Make read-only

        # Frame for buttons
        button_frame = ttk.Frame(win)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(button_frame, text="Close", command=win.destroy).pack(side=tk.RIGHT, padx=(5, 0))

        # AI Explanation Button (align right, next to close)
        # Pass the text content to the command function
        ai_button = ttk.Button(button_frame, text="🤖 Get AI Explanation",
                               command=lambda t=text_widget.get(1.0, tk.END), s=is_safe, seq=safe_sequence, f=finish_list: \
                                        self.get_ai_explanation(t, s, seq, f))
        ai_button.pack(side=tk.RIGHT, padx=(0, 5))

        if not self.ai_enabled:
            ai_button.config(state=tk.DISABLED)
        
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
            x, y = 200, 100 + i * spacing
            self.canvas.create_oval(x, y, x + node_size, y + node_size,
                                    fill="#2196F3", outline="#1976D2", width=2)
            self.canvas.create_text(x + node_size / 2, y + node_size / 2,
                                    text=f"P{i}", fill="white",
                                    font=('Segoe UI', 10, 'bold'))
            process_nodes[i] = (x + node_size, y + node_size / 2)

        # Draw resources (right side)
        for j in range(m):
            x, y = 700, 100 + j * spacing 
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
    
    def get_ai_explanation(self, explanation_text, is_safe, safe_sequence, finish_list):
        """Calls the Gemini API to get an explanation."""
        if not self.ai_enabled:
            messagebox.showerror("AI Error", "AI feature is disabled (check API key configuration).")
            return

        # Optional: Add a simple "loading" popup here if you want user feedback
        print("Contacting Gemini AI...") # Simple console feedback

        try:
            # Initialize the model
            # Make sure you have 'gemini-1.5-flash-latest' available or choose another model
            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            # --- Prompt ---
            # This tells the AI what to do with the text you send it
            if is_safe:
            # Use the actual sequence found by your code
                state_summary = f"Good news! The system is currently in a SAFE state. This means there's a guaranteed way for all processes ({', '.join(safe_sequence)}) to finish without getting stuck forever."
                details_section = f"""
    How the Safe Sequence Works ({' -> '.join(safe_sequence)}):
    Think of it like a well-managed queue. Here's the idea:
    1. The system looks at the first process in the sequence. It checks if the resources currently 'Available' are enough to satisfy what that process still 'Needs'.
    2. Because the state is safe, there *are* enough resources. So, the process gets what it needs, does its work, and finishes.
    3. When it's done, it releases all the resources it was using (its 'Allocation'). This is key!
    4. These released resources are added back to the 'Available' pool.
    5. Now the system looks at the *next* process in the sequence. Because the previous one released resources, there's a better chance the system has enough for this next one.
    6. This continues down the line. Each process running and releasing resources makes it possible for the next one to go. This prevents a situation where everyone is waiting for resources held by someone else who's also waiting (that's deadlock!).
    """
                analogy_request = "Explain this safe state using a simple, everyday analogy. For example, think about sharing limited tools in a workshop where people return tools promptly, allowing others to use them, or maybe a single-lane bridge with a good traffic light system."
            else:
                # Use the actual list of potentially blocked processes
                blocked_pids = [f'P{i}' for i, finished in enumerate(finish_list) if not finished]
                state_summary = f"Looks like the system is in an UNSAFE state. This is a warning sign! It means the system *cannot guarantee* that all processes will be able to finish. There's a risk they could get stuck in a deadlock. The processes that might get stuck are: {', '.join(blocked_pids)}."
                details_section = f"""
    Why it's Unsafe (Risk of Deadlock):
    Let's look at the processes that couldn't be guaranteed to finish ({', '.join(blocked_pids)}):
    1. Check the simulation data to see what resources each of these processes still 'Needs'.
    2. Compare that to the resources that were 'Available' in the system when the simulation realized it couldn't find another process to run safely.
    3. The problem is that the 'Available' resources are *not enough* to meet the 'Need' of *any* of these waiting processes.
    4. So, they all have to wait. But the resources they are waiting for might be held by *other waiting processes*!
    5. This creates a potential 'circular wait' – everyone is stuck waiting for someone else who is also stuck waiting. That's the essence of deadlock. The system can't promise a way out of this situation from this state.
    """
                analogy_request = "Explain this unsafe state using a simple, everyday analogy. Imagine a traffic jam in a small intersection where four cars all want to go straight, but each one blocks the car to its right – nobody can move! Or maybe two people who each have one of two keys needed to open a box, but they need the other person's key first."

            prompt = f"""
    You are a friendly and helpful Operating Systems assistant explaining the results of a Banker's Algorithm simulation. Use clear, simple language and focus on making the concepts easy to grasp.

    Here's the simulation data I have:
    --- Simulation Data ---
    {explanation_text}
    --- End Simulation Data ---

    Please explain the following based *only* on the data provided. Use the headings I've provided below and write in plain text (no bolding or other markdown formatting):

    What's the Situation? (System State)
    {state_summary} Is the system safe or unsafe? What does that mean in simple terms for the processes trying to run?

    How it Works or Doesn't (Detailed Explanation)
    {details_section} If it's safe, explain step-by-step how the safe sequence allows processes to finish. If it's unsafe, explain clearly why processes might get stuck, pointing to the 'Need' vs 'Available' issue from the data.

    Think of it Like This: (Analogy)
    {analogy_request} Give a simple, relatable real-world analogy that matches whether the state was safe or unsafe.

    Bottom Line: (Conclusion)
    In one sentence, what's the main takeaway about how well the system is handling its resources in this specific scenario?

    Remember to be clear, helpful, and use plain text only!
    """
            # <<< --- END OF NEW PROMPT SECTION --- >>>

            # --- Make API Call (remains the same) ---
            response = model.generate_content(prompt)

            print("AI Response Received.")
            # --- Display the Response (remains the same) ---
            self.show_ai_result(response.text)

        except Exception as e:
            messagebox.showerror("AI API Error", f"Failed to get explanation from AI: {str(e)}")
            print(f"Gemini API Error: {e}") # Log details to console
    # <<< --- END OF NEW METHOD --- >>>
    # <<< --- ADD THIS ENTIRE METHOD --- >>>
    def show_ai_result(self, ai_text):
        """Displays the AI's explanation in a new window."""
        ai_win = tk.Toplevel(self.root)
        ai_win.title("🤖 AI Explanation")
        ai_win.geometry("850x650") # Adjust size as needed
        text_frame = ttk.Frame(ai_win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 5)) # Increased padding
        # Use ScrolledText for potentially long responses
        ai_widget = scrolledtext.ScrolledText(text_frame, width=90, height=30, wrap=tk.WORD,
                                              bg="#424242", # Medium-dark grey background
                                              fg="#F5F5F5", # Light grey/off-white text (good contrast)
                                              insertbackground="white", # White cursor
                                              font=("Segoe UI", 11)) # Slightly larger, readable font
        ai_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ai_widget.insert(tk.END, ai_text)
        ai_widget.config(state=tk.DISABLED) # Make read-only

        # Add a close button to this window too
        button_frame = ttk.Frame(ai_win)
        button_frame.pack(fill=tk.X, padx=15, pady=(5, 10))
        ttk.Button(button_frame, text="Close", command=ai_win.destroy).pack(side=tk.RIGHT)

        ai_win.transient(self.root) # Keep on top
        ai_win.grab_set()          # Focus this window
        self.root.wait_window(ai_win)
    # <<< --- END OF NEW METHOD --- >>>

if __name__ == "__main__":
    root = tk.Tk()
    app = BankersGUI(root)
    root.mainloop()
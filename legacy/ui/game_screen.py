import tkinter as tk
from tkinter import messagebox
import random
from game import Game
from ui.scrollable_frame import ScrollableFrame
from ui.spin_grid import SpinGridCanvas
from constants import (
    COLOR_DARK_BLUE, COLOR_LIGHT_GRAY, COLOR_BLUE, COLOR_DARK_BLUE_HOVER,
    COLOR_ORANGE, COLOR_ORANGE_HOVER, COLOR_RED, COLOR_RED_HOVER,
    COLOR_GRAY, COLOR_GRAY_HOVER, COLOR_GREEN, COLOR_GREEN_HOVER,
    COLOR_YELLOW, COLOR_DIVIDER, COLOR_WHITE
)

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_DARK_BLUE)
        self.controller = controller
        
        self.game = None
        self.active_grid = None
        self.grids = []
        
        self.grid_height = 2
        self.grid_width = 2
        
        self.create_layout()
        
    def set_dimensions(self, h, w):
        self.grid_height = h
        self.grid_width = w
        
    def start_new_game(self):
        for widget in self.scroll_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.grids.clear()
        
        num_couplings = self.grid_height*(self.grid_width-1) + (self.grid_height-1)*self.grid_width
        solution = random.choices([0, 1], k=num_couplings)
        self.game = Game(solution, width=self.grid_width, height=self.grid_height)
        
        self.submit_spins_btn.config(state="normal")
        self.guess_couplings_btn.config(state="normal")
        self.submit_couplings_btn.config(state="disabled")
        
        self.add_spin_grid()
        self.update_ui()
        
    def create_layout(self):
        self.top_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        self.top_frame.pack(fill="x", padx=20, pady=15)
        
        quit_btn = tk.Button(self.top_frame, text="Quit Application", command=self.controller.quit_app, font=("Arial", 16), bg=COLOR_RED, fg="white", relief="flat", padx=10, pady=5)
        quit_btn.pack(side="left")
        
        back_btn = tk.Button(self.top_frame, text="Back to Menu", command=lambda: self.controller.show_frame("StartMenu"), font=("Arial", 16), bg=COLOR_GRAY, fg="white", relief="flat", padx=10, pady=5)
        back_btn.pack(side="right")
        
        self.body_frame = tk.Frame(self, bg=COLOR_DARK_BLUE)
        self.body_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.scroll_frame = ScrollableFrame(self.body_frame)
        self.scroll_frame.pack(side="left", fill="both", expand=True)
        
        self.control_frame = tk.Frame(self.body_frame, bg=COLOR_LIGHT_GRAY, padx=30, pady=30, width=400)
        self.control_frame.pack(side="right", fill="y", padx=(20, 0))
        self.control_frame.pack_propagate(False)
        
        tk.Label(self.control_frame, text="Ising Game", font=("Arial", 36, "bold"), bg=COLOR_LIGHT_GRAY, fg=COLOR_DARK_BLUE).pack(pady=(0, 20))
        
        self.tries_label = tk.Label(self.control_frame, text="Tries left: 0", font=("Arial", 24), bg=COLOR_LIGHT_GRAY, fg=COLOR_DARK_BLUE_HOVER)
        self.tries_label.pack(pady=20)
        
        self.submit_spins_btn = tk.Button(self.control_frame, text="Submit Spin Guess", command=self.submit_spins, font=("Arial", 20, "bold"), bg=COLOR_BLUE, fg="white", activebackground=COLOR_DARK_BLUE_HOVER, relief="flat", padx=10, pady=15)
        self.submit_spins_btn.pack(pady=25, fill="x")
        
        tk.Frame(self.control_frame, height=3, bd=0, bg=COLOR_DIVIDER).pack(fill="x", padx=10, pady=30)
        
        self.guess_couplings_btn = tk.Button(self.control_frame, text="Guess Couplings", command=self.start_couplings_mode, font=("Arial", 20, "bold"), bg=COLOR_ORANGE, fg="white", activebackground=COLOR_ORANGE_HOVER, relief="flat", padx=10, pady=15)
        self.guess_couplings_btn.pack(pady=25, fill="x")
        
        self.submit_couplings_btn = tk.Button(self.control_frame, text="Submit Couplings", command=self.submit_couplings, font=("Arial", 20, "bold"), bg=COLOR_GREEN, fg="white", activebackground=COLOR_GREEN_HOVER, relief="flat", state="disabled", padx=10, pady=15)
        self.submit_couplings_btn.pack(pady=25, fill="x")
        
    def add_spin_grid(self):
        row_frame = tk.Frame(self.scroll_frame.scrollable_frame, bg=COLOR_DARK_BLUE, pady=15)
        row_frame.pack(pady=10)
        
        grid = SpinGridCanvas(row_frame, mode="SPINS", height_cells=self.grid_height, width_cells=self.grid_width)
        grid.pack(side="left", padx=40)
        
        info_frame = tk.Frame(row_frame, bg=COLOR_DARK_BLUE)
        info_frame.pack(side="left", padx=20, fill="y")
        
        info_label = tk.Label(info_frame, text="Energy: ?", font=("Arial", 28, "bold"), bg=COLOR_DARK_BLUE, fg=COLOR_LIGHT_GRAY)
        info_label.pack(anchor="w", pady=(85, 0)) 
        
        self.active_grid = grid
        self.grids.append((grid, info_label))
        
        self.update_idletasks()
        self.scroll_frame.canvas.yview_moveto(1.0)
        
    def update_ui(self):
        self.tries_label.config(text=f"Tries left: {self.game.get_remaining_tries()}")
        
    def submit_spins(self):
        if self.game.get_remaining_tries() <= 0:
            messagebox.showinfo("Game Over", "You have zero tries left! You lost!")
            return
            
        spins = self.active_grid.get_spins()
        energy = self.game.input_spins(spins)
        
        self.active_grid.lock()
        _, label = self.grids[-1]
        label.config(text=f"Energy: {energy}", fg=COLOR_YELLOW) 
        
        self.update_ui()
        
        if self.game.get_remaining_tries() > 0:
            self.add_spin_grid()
        else:
            messagebox.showinfo("Out of Tries", "You have zero tries left for spins! Let's guess couplings.")
            self.start_couplings_mode()
            
    def start_couplings_mode(self):
        self.submit_spins_btn.config(state="disabled")
        self.guess_couplings_btn.config(state="disabled")
        self.submit_couplings_btn.config(state="normal")
        
        self.game.toggle_input_state()
        
        if self.active_grid:
            self.active_grid.mode = "COUPLINGS"
            _, label = self.grids[-1]
            label.config(text="Guessing Couplings...")
            label.config(fg=COLOR_GREEN)
            
    def submit_couplings(self):
        couplings = self.active_grid.get_couplings()
        if None in couplings:
            messagebox.showwarning("Incomplete", "Please assign (+ or -) to all bonds!\n\nClick the grey blocks between the arrows.")
            return
            
        correct = self.game.input_couplings(couplings)
        self.active_grid.lock()
        
        if correct:
            self.controller.trigger_fireworks()
        else:
            answer = self.game.get_solution().get_couplings()
            
            top = tk.Toplevel(self.winfo_toplevel())
            top.title("Game Over")
            top.configure(bg=COLOR_DARK_BLUE)
            
            tk.Label(top, text="This guess is wrong, you lose the game!\n\nThe correct couplings were:", font=("Arial", 20, "bold"), bg=COLOR_DARK_BLUE, fg=COLOR_RED).pack(pady=20, padx=20)
            
            ans_grid = SpinGridCanvas(top, mode="LOCKED", height_cells=self.grid_height, width_cells=self.grid_width, show_arrows=False)
            ans_grid.couplings = answer
            ans_grid.draw_grid()
            ans_grid.pack(padx=40, pady=(0, 40))
            
        self.submit_couplings_btn.config(state="disabled")

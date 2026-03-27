import tkinter as tk
from tkinter import messagebox
import random
import time
from game import Game
from enums.inputstate import InputState

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg="#2C3E50")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2C3E50")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

class SpinGridCanvas(tk.Canvas):
    def __init__(self, parent, mode="SPINS", height_cells=2, width_cells=2, **kwargs):
        self.mode = mode
        self.h_cells = height_cells
        self.w_cells = width_cells
        
        # Initialize arrows pointing UP
        self.spins = [[1]*self.w_cells for _ in range(self.h_cells)] 
        
        self.num_couplings = self.h_cells*(self.w_cells-1) + (self.h_cells-1)*self.w_cells
        self.couplings = [None] * self.num_couplings
        
        self.cell_size = 60
        self.margin = 40
        self.gap = 40
        
        cw = 2*self.margin + self.w_cells*self.cell_size + (self.w_cells-1)*self.gap
        ch = 2*self.margin + self.h_cells*self.cell_size + (self.h_cells-1)*self.gap
        
        super().__init__(parent, width=cw, height=ch, bg="#34495E", highlightthickness=0, **kwargs)
        
        self.bind("<Button-1>", self.on_click)
        self.draw_grid()
        
    def draw_grid(self):
        self.delete("all")
        for i in range(self.num_couplings):
            self.draw_coupling(i)
        for r in range(self.h_cells):
            for c in range(self.w_cells):
                self.draw_arrow(r, c)
                
    def get_arrow_center(self, r, c):
        cx = self.margin + c * (self.cell_size + self.gap) + self.cell_size/2
        cy = self.margin + r * (self.cell_size + self.gap) + self.cell_size/2
        return cx, cy

    def draw_arrow(self, r, c):
        cx, cy = self.get_arrow_center(r, c)
        is_up = self.spins[r][c] == 1
        
        color = "#E74C3C" if is_up else "#3498DB" # Red up, blue down
        
        w = self.cell_size * 0.4
        h = self.cell_size * 0.8
        
        if is_up:
            pts = [
                cx, cy - h/2,
                cx + w/2, cy - h/6,
                cx + w/6, cy - h/6,
                cx + w/6, cy + h/2,
                cx - w/6, cy + h/2,
                cx - w/6, cy - h/6,
                cx - w/2, cy - h/6
            ]
        else:
            pts = [
                cx, cy + h/2,
                cx + w/2, cy + h/6,
                cx + w/6, cy + h/6,
                cx + w/6, cy - h/2,
                cx - w/6, cy - h/2,
                cx - w/6, cy + h/6,
                cx - w/2, cy + h/6
            ]
            
        tag = f"arrow_{r}_{c}"
        self.create_polygon(pts, fill=color, outline="white", width=2, tags=tag, joinstyle=tk.ROUND)
        
    def get_coupling_rect(self, idx):
        num_horiz = self.h_cells * (self.w_cells - 1)
        w = self.gap * 0.9
        h = self.gap * 0.7
        
        if idx < num_horiz:
            # Horizontal coupling
            r = idx // (self.w_cells - 1)
            c = idx % (self.w_cells - 1)
            
            c1x, c1y = self.get_arrow_center(r, c)
            c2x, c2y = self.get_arrow_center(r, c + 1)
            
            cx = (c1x + c2x) / 2
            cy = c1y
            return cx-w/2, cy-h/2, cx+w/2, cy+h/2
        else:
            # Vertical coupling
            v_idx = idx - num_horiz
            r = v_idx // self.w_cells
            c = v_idx % self.w_cells
            
            c1x, c1y = self.get_arrow_center(r, c)
            c2x, c2y = self.get_arrow_center(r + 1, c)
            
            cx = c1x
            cy = (c1y + c2y) / 2
            return cx-h/2, cy-w/2, cx+h/2, cy+w/2

    def draw_coupling(self, idx):
        val = self.couplings[idx]
        x1, y1, x2, y2 = self.get_coupling_rect(idx)
        
        bg_color = "#7F8C8D"
        text = ""
        if val == 1:
            bg_color = "#2ECC71"
            text = "+"
        elif val == 0:
            bg_color = "#E74C3C"
            text = "-"
            
        tag = f"comp_{idx}"
        self.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#2C3E50", width=3, tags=tag)
        if text:
            cx, cy = (x1+x2)/2, (y1+y2)/2
            self.create_text(cx, cy, text=text, fill="white", font=("Arial", 16, "bold"), tags=tag)

    def on_click(self, event):
        if self.mode == "LOCKED":
            return
            
        x, y = event.x, event.y
        
        if self.mode == "SPINS":
            for r in range(self.h_cells):
                for c in range(self.w_cells):
                    cx, cy = self.get_arrow_center(r, c)
                    if abs(x - cx) < self.cell_size/2 and abs(y - cy) < self.cell_size/2:
                        self.spins[r][c] = 1 - self.spins[r][c]
                        self.draw_grid()
                        return
                        
        elif self.mode == "COUPLINGS":
            # Just listen to the coupling line clicks
            for i in range(self.num_couplings):
                x1, y1, x2, y2 = self.get_coupling_rect(i)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    current = self.couplings[i]
                    if current is None:
                        self.couplings[i] = 1
                    elif current == 1:
                        self.couplings[i] = 0
                    else:
                        self.couplings[i] = None
                    self.draw_grid()
                    return

    def get_spins(self):
        return self.spins
        
    def get_couplings(self):
        return self.couplings
        
    def lock(self):
        self.mode = "LOCKED"


class StartMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        
        # We need an inner frame to center things
        center_frame = tk.Frame(self, bg="#2C3E50")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="Ising Game", font=("Arial", 64, "bold"), bg="#2C3E50", fg="#ECF0F1")
        title.pack(pady=(0, 50))
        
        start_btn = tk.Button(center_frame, text="Start New Game", command=lambda: controller.show_frame("LevelSelectScreen"), font=("Arial", 24), bg="#3498DB", fg="white", activebackground="#2980B9", relief="flat", padx=20, pady=10, width=15)
        start_btn.pack(pady=15)
        
        tutorial_btn = tk.Button(center_frame, text="Tutorial", command=lambda: controller.show_frame("TutorialScreen"), font=("Arial", 24), bg="#F39C12", fg="white", activebackground="#E67E22", relief="flat", padx=20, pady=10, width=15)
        tutorial_btn.pack(pady=15)
        
        quit_btn = tk.Button(center_frame, text="Quit Game", command=controller.quit_app, font=("Arial", 24), bg="#E74C3C", fg="white", activebackground="#C0392B", relief="flat", padx=20, pady=10, width=15)
        quit_btn.pack(pady=15)

class LevelSelectScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        
        center_frame = tk.Frame(self, bg="#2C3E50")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="Select Difficulty", font=("Arial", 48, "bold"), bg="#2C3E50", fg="#ECF0F1")
        title.pack(pady=(0, 40))
        
        levels = [
            ("Level 0 (1x3)", 1, 3),
            ("Level 1 (2x2)", 2, 2),
            ("Level 2 (3x2)", 3, 2),
            ("Level 3 (3x3)", 3, 3)
        ]
        
        for name, h, w in levels:
            btn = tk.Button(center_frame, text=name, 
                            command=lambda height=h, width=w: self.start_level(height, width), 
                            font=("Arial", 20), bg="#3498DB", fg="white", 
                            activebackground="#2980B9", relief="flat", padx=20, pady=10, width=15)
            btn.pack(pady=10)
            
        back_btn = tk.Button(center_frame, text="Back", command=lambda: controller.show_frame("StartMenu"), font=("Arial", 20), bg="#7F8C8D", fg="white", activebackground="#95A5A6", relief="flat", padx=20, pady=10, width=15)
        back_btn.pack(pady=(30,0))
        
    def start_level(self, height, width):
        self.controller.frames["GameScreen"].set_dimensions(height, width)
        self.controller.show_frame("GameScreen")

class TutorialScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        
        # Top Nav
        top_frame = tk.Frame(self, bg="#2C3E50")
        top_frame.pack(fill="x", padx=20, pady=20)
        
        quit_btn = tk.Button(top_frame, text="Quit Application", command=controller.quit_app, font=("Arial", 16), bg="#E74C3C", fg="white", relief="flat", padx=10, pady=5)
        quit_btn.pack(side="left")
        
        back_btn = tk.Button(top_frame, text="Back to Menu", command=lambda: controller.show_frame("StartMenu"), font=("Arial", 16), bg="#7F8C8D", fg="white", relief="flat", padx=10, pady=5)
        back_btn.pack(side="right")
        
        title = tk.Label(self, text="Tutorial", font=("Arial", 48, "bold"), bg="#2C3E50", fg="#ECF0F1")
        title.pack(pady=(50, 20))
        
        placeholder = tk.Label(self, text="Placeholder text for now.\nRules and guides will be written here later.", font=("Arial", 28), bg="#2C3E50", fg="#BDC3C7")
        placeholder.pack(pady=50)

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
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
        # Clear scroll history
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
        # Top Nav
        self.top_frame = tk.Frame(self, bg="#2C3E50")
        self.top_frame.pack(fill="x", padx=20, pady=15)
        
        quit_btn = tk.Button(self.top_frame, text="Quit Application", command=self.controller.quit_app, font=("Arial", 16), bg="#E74C3C", fg="white", relief="flat", padx=10, pady=5)
        quit_btn.pack(side="left")
        
        back_btn = tk.Button(self.top_frame, text="Back to Menu", command=lambda: self.controller.show_frame("StartMenu"), font=("Arial", 16), bg="#7F8C8D", fg="white", relief="flat", padx=10, pady=5)
        back_btn.pack(side="right")
        
        # Content body
        self.body_frame = tk.Frame(self, bg="#2C3E50")
        self.body_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left side: Scrollable Canvas Frame
        self.scroll_frame = ScrollableFrame(self.body_frame)
        self.scroll_frame.pack(side="left", fill="both", expand=True)
        
        # Right side: Control Panel
        self.control_frame = tk.Frame(self.body_frame, bg="#ECF0F1", padx=30, pady=30, width=400)
        self.control_frame.pack(side="right", fill="y", padx=(20, 0))
        self.control_frame.pack_propagate(False)
        
        tk.Label(self.control_frame, text="Ising Game", font=("Arial", 36, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=(0, 20))
        
        self.tries_label = tk.Label(self.control_frame, text="Tries left: 0", font=("Arial", 24), bg="#ECF0F1", fg="#2980B9")
        self.tries_label.pack(pady=20)
        
        self.submit_spins_btn = tk.Button(self.control_frame, text="Submit Spin Guess", command=self.submit_spins, font=("Arial", 20, "bold"), bg="#3498DB", fg="white", activebackground="#2980B9", relief="flat", padx=10, pady=15)
        self.submit_spins_btn.pack(pady=25, fill="x")
        
        tk.Frame(self.control_frame, height=3, bd=0, bg="#BDC3C7").pack(fill="x", padx=10, pady=30)
        
        self.guess_couplings_btn = tk.Button(self.control_frame, text="Guess Couplings", command=self.start_couplings_mode, font=("Arial", 20, "bold"), bg="#F39C12", fg="white", activebackground="#E67E22", relief="flat", padx=10, pady=15)
        self.guess_couplings_btn.pack(pady=25, fill="x")
        
        self.submit_couplings_btn = tk.Button(self.control_frame, text="Submit Couplings", command=self.submit_couplings, font=("Arial", 20, "bold"), bg="#2ECC71", fg="white", activebackground="#27AE60", relief="flat", state="disabled", padx=10, pady=15)
        self.submit_couplings_btn.pack(pady=25, fill="x")
        
    def add_spin_grid(self):
        row_frame = tk.Frame(self.scroll_frame.scrollable_frame, bg="#2C3E50", pady=15)
        row_frame.pack(fill="x", pady=10)
        
        grid = SpinGridCanvas(row_frame, mode="SPINS", height_cells=self.grid_height, width_cells=self.grid_width)
        grid.pack(side="left", padx=40)
        
        info_frame = tk.Frame(row_frame, bg="#2C3E50")
        info_frame.pack(side="left", padx=20, fill="y", expand=True)
        
        info_label = tk.Label(info_frame, text="Energy: ?", font=("Arial", 28, "bold"), bg="#2C3E50", fg="#ECF0F1")
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
        label.config(text=f"Energy: {energy}", fg="#F1C40F") 
        
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
            self.active_grid.mode = "COUPLINGS" # Let the arrows stay as they currently are.
            _, label = self.grids[-1]
            label.config(text="Guessing Couplings...")
            label.config(fg="#2ECC71")
            
    def submit_couplings(self):
        couplings = self.active_grid.get_couplings()
        if None in couplings:
            messagebox.showwarning("Incomplete", "Please assign (+ or -) to all 4 lines!\n\nClick the grey blocks between the arrows.")
            return
            
        correct = self.game.input_couplings(couplings)
        self.active_grid.lock()
        
        if correct:
            self.controller.trigger_fireworks()
        else:
            answer = self.game.get_solution().get_couplings()
            ans_str = ["+" if x==1 else "-" for x in answer]
            msg = f"This guess is wrong, you lose the game!\n\nThe correct answer was:\n{', '.join(ans_str)}"
            messagebox.showinfo("Result", msg)
            
        self.submit_couplings_btn.config(state="disabled")


class FireworksAnimation(tk.Canvas):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self.particles = []
        self.is_running = True
        
        # After a tiny delay to ensure window is laid out, blast off
        self.after(50, lambda: self.create_explosion(self.winfo_width() / 2, self.winfo_height() / 2))
        self.update_animation()
        
        self.after(3000, self.stop_animation)
        
    def create_explosion(self, cx, cy):
        colors = ["#F1C40F", "#E74C3C", "#9B59B6", "#3498DB", "#2ECC71", "#FFFFFF"]
        w = max(self.winfo_width(), 800)
        h = max(self.winfo_height(), 600)
        
        for _ in range(6):
            ex = random.randint(int(w*0.2), int(w*0.8))
            ey = random.randint(int(h*0.2), int(h*0.8))
            
            for _ in range(35):
                speed = random.uniform(3, 14)
                size = random.uniform(4, 9)
                color = random.choice(colors)
                
                dx = speed * random.uniform(-1, 1)
                dy = speed * random.uniform(-1, 1)
                
                p = self.create_oval(ex, ey, ex+size, ey+size, fill=color, outline="")
                self.particles.append({"id": p, "dx": dx, "dy": dy, "life": 100})
                
    def update_animation(self):
        if not self.is_running:
            return
            
        to_remove = []
        for p in self.particles:
            pid = p["id"]
            self.move(pid, p["dx"], p["dy"])
            p["dy"] += 0.25 # Gravity
            p["life"] -= 2
            
            if p["life"] <= 0:
                self.delete(pid)
                to_remove.append(p)
                
        for p in to_remove:
            self.particles.remove(p)
            
        if self.is_running:
            self.after(30, self.update_animation)
            
    def stop_animation(self):
        if not self.is_running:
            return
        self.is_running = False
        self.delete("all")
        self.destroy() 
        self.callback()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ising Game UI")
        # Enforce fullscreen requirement
        self.attributes('-fullscreen', True)
        self.configure(bg="#2C3E50")
        
        self.container = tk.Frame(self, bg="#2C3E50")
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        # Initializing the screens
        for F in (StartMenu, LevelSelectScreen, TutorialScreen, GameScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.show_frame("StartMenu")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        
        if page_name == "GameScreen":
            frame.start_new_game()
            
        frame.tkraise()
        
    def trigger_fireworks(self):
        w = self.winfo_width()
        h = self.winfo_height()
        fw_canvas = FireworksAnimation(self, callback=self.on_win_complete, width=w, height=h, bg="#2C3E50", highlightthickness=0)
        fw_canvas.place(x=0, y=0)
        
    def on_win_complete(self):
        messagebox.showinfo("Winner", "Congratulations, you successfully mapped the couplings!")
        
    def quit_app(self):
        self.destroy()

def start_gui():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    start_gui()

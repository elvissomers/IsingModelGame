import tkinter as tk
from constants import (
    CELL_SIZE, MARGIN_SIZE, GAP_SIZE,
    COLOR_SPIN_GRID_BG, COLOR_RED, COLOR_BLUE,
    COLOR_GRAY, COLOR_GREEN, COLOR_DARK_BLUE, COLOR_WHITE
)

class SpinGridCanvas(tk.Canvas):
    def __init__(self, parent, mode="SPINS", height_cells=2, width_cells=2, show_arrows=True, **kwargs):
        self.mode = mode
        self.grid_height = height_cells
        self.grid_width = width_cells
        self.show_arrows = show_arrows
        
        self.spins = [[1]*self.grid_width for _ in range(self.grid_height)] 
        
        self.num_couplings = self.grid_height*(self.grid_width-1) + (self.grid_height-1)*self.grid_width
        self.couplings = [None] * self.num_couplings
        
        canvas_width = 2*MARGIN_SIZE + self.grid_width*CELL_SIZE + (self.grid_width-1)*GAP_SIZE
        canvas_height = 2*MARGIN_SIZE + self.grid_height*CELL_SIZE + (self.grid_height-1)*GAP_SIZE
        
        super().__init__(parent, width=canvas_width, height=canvas_height, bg=COLOR_SPIN_GRID_BG, highlightthickness=0, **kwargs)
        
        self.bind("<Button-1>", self.on_click)
        self.draw_grid()
        
    def draw_grid(self):
        self.delete("all")
        for i in range(self.num_couplings):
            self.draw_coupling(i)
        if self.show_arrows:
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    self.draw_arrow(row, col)
                
    def get_arrow_center(self, row, col):
        center_x = MARGIN_SIZE + col * (CELL_SIZE + GAP_SIZE) + CELL_SIZE/2
        center_y = MARGIN_SIZE + row * (CELL_SIZE + GAP_SIZE) + CELL_SIZE/2
        return center_x, center_y

    def draw_arrow(self, row, col):
        center_x, center_y = self.get_arrow_center(row, col)
        is_up = self.spins[row][col] == 1
        
        color = COLOR_RED if is_up else COLOR_BLUE
        
        arrow_width = CELL_SIZE * 0.4
        arrow_height = CELL_SIZE * 0.8
        
        if is_up:
            points = [
                center_x, center_y - arrow_height/2,
                center_x + arrow_width/2, center_y - arrow_height/6,
                center_x + arrow_width/6, center_y - arrow_height/6,
                center_x + arrow_width/6, center_y + arrow_height/2,
                center_x - arrow_width/6, center_y + arrow_height/2,
                center_x - arrow_width/6, center_y - arrow_height/6,
                center_x - arrow_width/2, center_y - arrow_height/6
            ]
        else:
            points = [
                center_x, center_y + arrow_height/2,
                center_x + arrow_width/2, center_y + arrow_height/6,
                center_x + arrow_width/6, center_y + arrow_height/6,
                center_x + arrow_width/6, center_y - arrow_height/2,
                center_x - arrow_width/6, center_y - arrow_height/2,
                center_x - arrow_width/6, center_y + arrow_height/6,
                center_x - arrow_width/2, center_y + arrow_height/6
            ]
            
        tag = f"arrow_{row}_{col}"
        self.create_polygon(points, fill=color, outline=COLOR_WHITE, width=2, tags=tag, joinstyle=tk.ROUND)
        
    def get_coupling_rect(self, idx):
        num_horiz = self.grid_height * (self.grid_width - 1)
        size = GAP_SIZE * 0.7
        
        if idx < num_horiz:
            row = idx // (self.grid_width - 1)
            col = idx % (self.grid_width - 1)
            
            center1_x, center1_y = self.get_arrow_center(row, col)
            center2_x, center2_y = self.get_arrow_center(row, col + 1)
            
            center_x = (center1_x + center2_x) / 2
            center_y = center1_y
            return center_x-size/2, center_y-size/2, center_x+size/2, center_y+size/2
        else:
            v_idx = idx - num_horiz
            row = v_idx // self.grid_width
            col = v_idx % self.grid_width
            
            center1_x, center1_y = self.get_arrow_center(row, col)
            center2_x, center2_y = self.get_arrow_center(row + 1, col)
            
            center_x = center1_x
            center_y = (center1_y + center2_y) / 2
            return center_x-size/2, center_y-size/2, center_x+size/2, center_y+size/2

    def draw_coupling(self, idx):
        coupling_value = self.couplings[idx]
        x1, y1, x2, y2 = self.get_coupling_rect(idx)
        
        bg_color = COLOR_GRAY
        text = ""
        if coupling_value == 1:
            bg_color = COLOR_GREEN
            text = "+"
        elif coupling_value == 0:
            bg_color = COLOR_RED
            text = "-"
            
        tag = f"comp_{idx}"
        self.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=COLOR_DARK_BLUE, width=3, tags=tag)
        if text:
            center_x, center_y = (x1+x2)/2, (y1+y2)/2
            self.create_text(center_x, center_y, text=text, fill=COLOR_WHITE, font=("Arial", 16, "bold"), tags=tag)

    def on_click(self, event):
        if self.mode == "LOCKED":
            return
            
        x, y = event.x, event.y
        
        if self.mode == "SPINS":
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    center_x, center_y = self.get_arrow_center(row, col)
                    if abs(x - center_x) < CELL_SIZE/2 and abs(y - center_y) < CELL_SIZE/2:
                        self.spins[row][col] = 1 - self.spins[row][col]
                        self.draw_grid()
                        return
                        
        elif self.mode == "COUPLINGS":
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

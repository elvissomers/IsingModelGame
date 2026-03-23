from math import floor


class Configuration:
    """A configuration of spins (up or down) along some grid"""
    def __init__(self, width, height, spins_in_order):
        self.width = width
        self.height = height

        self.spins = [ [0] * width for i in range(height)]
        self.initialize_spins(spins_in_order)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def initialize_spins(self, spins_in_order):
        for i, spin in enumerate(spins_in_order):
            x_index = i % self.width
            y_index = floor(i/self.width)
            self.spins[y_index][x_index] = spin

    def get_spins(self):
        return self.spins
from math import floor


class Configuration:
    """A configuration of spins (up or down) along some grid"""
    def __init__(self, spins, width=2, height=2):
        self.width = width
        self.height = height
        self.spins = spins

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_spins(self):
        return self.spins


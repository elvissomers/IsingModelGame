from math import floor


class Solution:
    """A class containing all the J's for some Ising model"""
    def __init__(self, width, height, js_in_order):
        self.width = width
        self.height = height

        self.js_array = [ [0] * width*height for i in range(width*height)]
        # TODO : 2D array of all nodes? Or just of all connections? OR just 1D array to grid?
        # TODO: just use 1 different input? Not a list?
        self.initialize_js_array(js_in_order)

    def initialize_js_array(self, js_in_order):
        js_array = []
        for i, coupling in enumerate(js_in_order):
            x_index = i % self.width
            js_line = None
            if x_index == 0:
                size = 0
                y_index = floor(i / self.width)
                if y_index % 2 == 0:
                    size = self.width - 1
                else:
                    size = self.width
                js_line = [0]*size
            js_line[x_index] = coupling
            js_array.append(js_line)




    def getEnergy(self, configuration):
        energy = 0
        spins = configuration.get_spins()
        for i, coupling in enumerate(self.js_in_order):
            x_index = i % self.width
            y_index = floor(i / self.width)




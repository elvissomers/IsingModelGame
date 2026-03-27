class Solution:
    def __init__(self, couplings, width=2, height=2):
        self.width = width
        self.height = height
        self.couplings = couplings

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_couplings(self):
        return self.couplings

    def check_couplings(self, couplings):
        if self.couplings == couplings:
            return True
        else:
            return False

    def get_energy(self, spins):
        energy = 0
        coupling_index = 0

        # Horizontal couplings
        for r in range(self.height):
            for c in range(self.width - 1):
                if spins[r][c] != spins[r][c + 1]:
                    energy += self.couplings[coupling_index]
                else:
                    energy += 1 - self.couplings[coupling_index]
                coupling_index += 1

        # Vertical couplings
        for r in range(self.height - 1):
            for c in range(self.width):
                if spins[r][c] != spins[r + 1][c]:
                    energy += self.couplings[coupling_index]
                else:
                    energy += 1 - self.couplings[coupling_index]
                coupling_index += 1

        return energy


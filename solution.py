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

        if spins[0][0] != spins[0][1]:
            energy += self.couplings[0]
        else:
            energy += 1 - self.couplings[0]

        if spins[0][0] != spins[1][0]:
            energy += self.couplings[1]
        else:
            energy += 1 - self.couplings[1]

        if spins[0][1] != spins[1][1]:
            energy += self.couplings[2]
        else:
            energy += 1 - self.couplings[2]

        if spins[1][0] != spins[1][1]:
            energy += self.couplings[3]
        else:
            energy += 1 - self.couplings[3]

        return energy



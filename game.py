from enums.inputstate import InputState
from solution import Solution


class Game:
    def __init__(self, couplings):
        self.solution = Solution(couplings)
        self.input_state = InputState.SPINS
        self.remaining_tries = self.calculate_remaining_tries(couplings)

    def get_remaining_tries(self):
        return self.remaining_tries

    def get_solution(self):
        return self.solution

    @staticmethod
    def calculate_remaining_tries(solution):
        # todo: "reasonable" amount of tries
        return 2*len(solution)

    def toggle_input_state(self):
        if self.input_state == InputState.SPINS:
            self.input_state = InputState.COUPLINGS
        else:
            self.input_state = InputState.SPINS

    def input_spins(self, spins):
        self.remaining_tries = self.remaining_tries - 1
        return self.solution.get_energy(spins)

    def input_couplings(self, couplings):
        return self.solution.check_couplings(couplings)
from enums.inputstate import InputState


class Game:
    def __init__(self, solution):
        self.solution = solution
        self.input_state = InputState.SPINS
        self.remaining_tries = self.calculate_remaining_tries(solution)

    @staticmethod
    def calculate_remaining_tries(configuration):
        # todo: "reasonable" amount of tries
        return 2*configuration.get_width()*configuration.get_height()

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
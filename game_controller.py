import random
from game import Game


LEVEL_DIMS = {
    "0": (1, 3), # height 1, width 3
    "1": (2, 2), # height 2, width 2
    "2": (3, 2), # height 3, width 2
    "3": (3, 3)  # height 3, width 3
}

def start_new_game():
    level = input("Select Difficulty (0=1x3, 1=2x2, 2=3x2, 3=3x3): ").strip()
    if level not in LEVEL_DIMS:
        print("Invalid level, defaulting to Level 1 (2x2).")
        level = "1"
        
    height, width = LEVEL_DIMS[level]
    num_couplings = height*(width-1) + (height-1)*width
    solution = random.choices([0,1], k=num_couplings)
    game = Game(solution, width=width, height=height)

    while True:
        command = input("You can use the following commands: \n"
                        "(1): Input of spins as 1 (up) or 0 (down). \n"
                        "(2): Input of couplings as 1 (positive) or 0 (negative) \n"
                        "(q): To quit the game. \n ").strip().lower()

        if command == "1":
            print(f"Let's enter your spins row-by-row for the {height}x{width} grid:")
            guess_grid = []
            
            for r in range(height):
                guess = input(f"Enter row {r+1} (e.g. {','.join(['0']*width)}): ")
                row = list(map(int, guess.split(",")))
                guess_grid.append(row)
                
            energy = game.input_spins(guess_grid)
            tries_remaining = game.get_remaining_tries()
            print("The energy is: ", energy)
            if tries_remaining == 0:
                print("You have zero tries left! You lost!")
                break
            else:
                print("You have", tries_remaining, "tries left!")

        elif command == "2":
            print(f"Your model has {num_couplings} couplings.")
            guess = input("Enter your guess for the flat coupling array by commas.\n"
                          "(Horizontal row-by-row, then vertical column-by-column)\n"
                          f"For example: {','.join(['0']*num_couplings)}\n")
            guess = list(map(int, guess.split(",")))
            guess_correct = game.input_couplings(guess)
            if guess_correct:
                print("Congratulations, you win the game!")
            else:
                print("This guess is wrong, you lose the game!")
                answer = game.get_solution().get_couplings()
                print("The correct answer was: ", answer)
            break

        elif command == "q":
            print("Goodbye!")
            break

        else:
            print(f"Unknown command: '{command}'")

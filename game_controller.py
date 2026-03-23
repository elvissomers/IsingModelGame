import random
from game import Game


def start_new_game_2_by_2():
    solution = random.choices([0,1],k=4)
    game = Game(solution)

    while True:
        command = input("You can use the following commands: \n"
                        "(1): Input of spins as 1 (up) or 0 (down). \n"
                        "(2): Input of couplings as 1 (positive) or 0 (negative) \n"
                        "(q): To quit the game. \n ").strip().lower()

        if command == "1":
            guess = input("Enter your guess. Use the format left to right, top to bottom. \n"
                          "For example: 0,1,0,0 \n")
            flat = list(map(int, guess.split(",")))
            guess = [flat[i:i + 2] for i in range(0, len(flat), 2)]
            energy = game.input_spins(guess)
            tries_remaining = game.get_remaining_tries()
            print("The energy is: ", energy)
            if tries_remaining == 0:
                print("You have zero tries left! You lost!")
                break
            else:
                print("You have", tries_remaining, "tries left!")

        elif command == "2":
            guess = input("Enter your guess. Use the format left to right, top to bottom. \n"
                          "For example: 0,1,0,0 \n")
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

        elif command == "stefanos":
            print("Congratulations you won")
            break

        else:
            print(f"Unknown command: '{command}'")

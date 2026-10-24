"""Task 1: Text-based Number Guessing Game (conditional statements)."""
import random

LEVELS = {"1": ("Easy", 10, 7), "2": ("Medium", 50, 6), "3": ("Hard", 100, 5)}


def choose_level():
    while True:
        print("\nChoose difficulty:")
        print("  1. Easy   (1-10,  7 tries)")
        print("  2. Medium (1-50,  6 tries)")
        print("  3. Hard   (1-100, 5 tries)")
        choice = input("Your choice: ").strip()
        if choice in LEVELS:
            return LEVELS[choice]
        print("Invalid choice, please enter 1, 2 or 3.")


def play_round():
    name, high, tries = choose_level()
    secret = random.randint(1, high)
    attempts_left = tries
    print(f"\n{name} mode: I'm thinking of a number between 1 and {high}.")

    while attempts_left > 0:
        text = input(f"Guess ({attempts_left} tries left): ").strip()
        if not text.isdigit():
            print("Please enter a whole number.")
            continue
        guess = int(text)
        if guess < 1 or guess > high:
            print(f"Stay within 1 and {high}.")
            continue

        attempts_left -= 1
        if guess == secret:
            score = (attempts_left + 1) * 10
            print(f"Correct! You win. Score: {score}")
            return score
        elif guess < secret:
            print("Too low!")
        else:
            print("Too high!")
        # Hint when close
        if abs(guess - secret) <= max(1, high // 10) and guess != secret:
            print("  (You're very close!)")

    print(f"Out of tries. The number was {secret}.")
    return 0


def main():
    print("=== NUMBER GUESSING GAME ===")
    total = 0
    while True:
        total += play_round()
        print(f"Total score: {total}")
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()

"""Task 4: Temperature converter (Celsius <-> Fahrenheit)."""


def c_to_f(c):
    return c * 9 / 5 + 32


def f_to_c(f):
    return (f - 32) * 5 / 9


def read_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number, try again.")


def main():
    print("=== TEMPERATURE CONVERTER ===")
    while True:
        print("\n1. Celsius -> Fahrenheit\n2. Fahrenheit -> Celsius\n3. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            c = read_number("Enter temperature in Celsius: ")
            if c < -273.15:
                print("Below absolute zero - not physically possible.")
                continue
            print(f"{c:.2f} C = {c_to_f(c):.2f} F")
        elif choice == "2":
            f = read_number("Enter temperature in Fahrenheit: ")
            if f < -459.67:
                print("Below absolute zero - not physically possible.")
                continue
            print(f"{f:.2f} F = {f_to_c(f):.2f} C")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

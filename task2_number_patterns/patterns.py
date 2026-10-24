"""Task 2: Number patterns using loops."""


def right_triangle(n):
    for i in range(1, n + 1):
        print(" ".join(str(j) for j in range(1, i + 1)))


def inverted_triangle(n):
    for i in range(n, 0, -1):
        print(" ".join(str(j) for j in range(1, i + 1)))


def floyd_triangle(n):
    num = 1
    for i in range(1, n + 1):
        row = []
        for _ in range(i):
            row.append(str(num))
            num += 1
        print(" ".join(row))


def pyramid(n):
    rows = []
    for i in range(1, n + 1):
        up = [str(j) for j in range(1, i + 1)]
        down = [str(j) for j in range(i - 1, 0, -1)]
        rows.append(" ".join(up + down))
    width = len(rows[-1])
    for row in rows:
        print(row.center(width))


def diamond(n):
    pyramid(n)
    rows = []
    for i in range(n - 1, 0, -1):
        up = [str(j) for j in range(1, i + 1)]
        down = [str(j) for j in range(i - 1, 0, -1)]
        rows.append(" ".join(up + down))
    width = len(" ".join([str(j) for j in range(1, n + 1)] + [str(j) for j in range(n - 1, 0, -1)]))
    for row in rows:
        print(row.center(width))


PATTERNS = {
    "1": ("Right triangle", right_triangle),
    "2": ("Inverted triangle", inverted_triangle),
    "3": ("Floyd's triangle", floyd_triangle),
    "4": ("Number pyramid", pyramid),
    "5": ("Diamond", diamond),
}


def main():
    while True:
        print("\n=== NUMBER PATTERNS ===")
        for key, (name, _) in PATTERNS.items():
            print(f"  {key}. {name}")
        print("  0. Exit")
        choice = input("Choose a pattern: ").strip()
        if choice == "0":
            break
        if choice not in PATTERNS:
            print("Invalid choice.")
            continue
        size = input("Number of rows (1-9 recommended): ").strip()
        if not size.isdigit() or int(size) < 1:
            print("Enter a positive whole number.")
            continue
        print()
        PATTERNS[choice][1](int(size))


if __name__ == "__main__":
    main()

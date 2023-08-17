def get_numeric_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            value = int(input(prompt))


def main():
    while True:
        height = get_numeric_input("Height: ")
        if 1 <= height <= 8:
            break
        print("Height must be between 1 and 8.")

    for j in range(1, height + 1):
        # Print leading spaces
        for i in range(height - j):
            print(" ", end="")

        # Print left hashes
        for i in range(1, height - (height - j - 1)):
            print("#", end="")

        # Print middle spaces
        for i in range(2):
            print(" ", end="")

        # Print right hashes
        for i in range(1, height - (height - j - 1)):
            print("#", end="")

        print()  # Move to the next line


if __name__ == "__main__":
    main()

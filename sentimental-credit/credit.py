def get_digit_count(card_number):
    count = 0
    while card_number > 0:
        card_number //= 10
        count += 1
    return count


def main():
    card_number = int(input("Number: "))

    sum = 0
    digit_count = 0
    first_digit, second_digit = 0, 0

    while card_number > 0:
        digit = card_number % 10

        if digit_count % 2 == 0:
            sum += digit
        else:
            product = digit * 2
            sum += product % 10
            sum += product // 10

        second_digit = first_digit
        first_digit = digit

        card_number //= 10
        digit_count += 1

    if sum % 10 == 0:
        if (
            digit_count == 15
            and first_digit == 3
            and (second_digit == 4 or second_digit == 7)
        ):
            print("AMEX")
        elif digit_count == 16 and first_digit == 5 and 1 <= second_digit <= 5:
            print("MASTERCARD")
        elif (digit_count == 13 or digit_count == 16) and first_digit == 4:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


if __name__ == "__main__":
    main()

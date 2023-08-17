#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long long card_number;

    card_number = get_long("Number: ");

    int sum = 0;
    int digit_count = 0;
    int first_digit, second_digit;

    while (card_number > 0)
    {
        int digit = card_number % 10;

        if (digit_count % 2 == 0)
        {
            sum += digit;
        }
        else
        {
            int product = digit * 2;

            sum += product % 10;
            sum += product / 10;
        }

        second_digit = first_digit;
        first_digit = digit;

        card_number /= 10;
        digit_count++;
    }

    if (sum % 10 == 0)
    {
        if (digit_count == 15 && (first_digit == 3 && (second_digit == 4 || second_digit == 7)))
        {
            printf("AMEX\n");
        }
        else if (digit_count == 16 && (first_digit == 5 && second_digit >= 1 && second_digit <= 5))
        {
            printf("MASTERCARD\n");
        }
        else if ((digit_count == 13 || digit_count == 16) && first_digit == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}

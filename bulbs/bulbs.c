#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int num);

int main(void)
{
    int val = 0;
    string s = get_string("Message: ");
    // string s = "HI!";
    for (int i = 0; i < strlen(s); i++)
    {
        val = s[i];
        print_bulb(val);
    }
}

void print_bulb(int num)
{
    int bit;
    for (int i = 7; i >= 0; i--)
    {
        bit = (num >> i) & 1;
        if (bit == 0)
        {
            printf("\U000026AB");
        }
        else if (bit == 1)
        {
            printf("\U0001F7E1");
        }
    }
    printf("\n");
}
#include <stdio.h>
#include <cs50.h>

int main()
{
    int hight;

    do
    {
        hight = get_int("Hight: ");
    }
    while (hight > 8 || hight < 1);

    for (int j = 1; j < hight + 1; j++)
    {
        for (int i = 0; i < (hight - j); i++)
        {
            printf(" ");
        }

        for (int i = 1; i < hight - (hight - j - 1); i++)
        {
            printf("#");
        }
        for (int i = 1; i < 2; i++)
        {
            printf("  ");
        }
        for (int i = 1; i < hight - (hight - j - 1); i++)
        {
            printf("#");
        }
        printf("\n");
    }
}
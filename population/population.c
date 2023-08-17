#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start, end, new, increment;
    do
    {
        start = get_int("Start Size= ");
    }
    while (start < 9);

    // TODO: Prompt for end size
    do
    {
        end = get_int("End size= ");
    }
    while (end < start);

    // TODO: Calculate number of years until we reach threshold
    // Each year increament in the population
    // Start inintially
    int n = 0;

    while (start < end)
    {
        float inc = (start / 3) - (start / 4);
        start = start + inc;
        // printf("%i\n", start);
        n++;
    }

    // TODO: Print number of years
    printf("Years: %i", n);
}
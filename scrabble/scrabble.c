#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};


int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!");
    }
    else
    {
        printf("Tie");
    }
}

int compute_score(string word)
{
    int var = 0;
    int sum = 0;
    // TODO: Compute and return score for string
    // Calculating length of a string
    int len = (int) strlen(word);
    // int len2 = (int) strlen(word2);

    // Printing letters of a string
    for (int n = 0; n < len; n++)
    {
        var = word[n];

        if (var < 65)
        {
            sum = sum + 0;
        }

        else if (var >= 65)
        {
            if (var <= 90)
            {
                sum = sum + POINTS[(int)var - (int)65];
            }

            else if (var > 90)
            {
                if (var <= 122)
                {
                    sum = sum + POINTS[(int)var - (int)97];
                }
                else if (var > 122)
                {
                    sum = sum + 0;
                }
            }
        }
    }
    return sum;
}

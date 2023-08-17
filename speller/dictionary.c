// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;
// Prototypes
unsigned int hash(const char *word);

// TODO: Choose number of buckets in hash table
const unsigned int N = 187751; // odd prime number bigger than word count, because math

// Hash table
node *table[N]; // may need to use calloc

// word count
int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // debug
    // int hashcode = hash(word);
    // printf("bucket: %i, word: %s\n", hash(word), table[hash(word)]->word);
    for (node *tmp = table[hash(word)]; tmp != NULL; tmp = tmp->next) // iterate through bucket
    {
        if (strcasecmp(tmp->word, word) == 0) // compare strings
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // Used Data Structures youtube course of Dr. Rob Edwards from San Diego State University mostly
    int hash = 0;
    /*int w = 0;
    //convert to upper case
    while (word[w] != '\0')
    {
        word[w] = toupper(word[w]);
        w++;
    }*/
    for (int i = 0; i <= strlen(word); i++)
    {
        hash = (31 * hash + toupper(word[i])) % N; // 31 because math
        // check hash size
        /*if (hash >= N)
            {
                printf("incorrect hash!");
            }*/
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // open dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        // printf("Could not open file.\n");
        return false;
    }
    // create temp string for word
    char *word = malloc(LENGTH + 1);
    if (word == NULL)
    {
        return false;
    }
    // read words from dictionary and write to hash table
    while (fscanf(dict, "%s", word) != EOF)
    {
        // node *tmp_word = NULL;
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        int pos = hash(word);   // run hash to find the bucket in table
        strcpy(n->word, word);  // write word to temp node
        if (table[pos] == NULL) // check if node is first in bucket (may need to use calloc to create a table)
        {
            n->next = NULL;
        }
        else // if not the first, write node to the head
        {
            n->next = table[pos]; // reference first node
        }
        table[pos] = n; // write node to table
        word_count++;   // count new word
    }
    fclose(dict);
    free(word);
    // debug
    /*int j = 0;
    while (j <= 11)
    {
        for (node *tmp = table[j]; tmp != NULL; tmp = tmp->next) //делаем ноду; пока не дойдем до последней; переходим к следующей
                {
                    printf("%s\n", tmp->word); //забираем значение ноды

                }
        printf("Bucket number: %i\n", j);
        j++;
    }*/
    // printf("word count:%i\n", word_count);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i <= N; i++)
    {
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next; //делаем ноду и переходим на следующую ячейку
            free(table[i]);             //освобождаем текущую
            table[i] = tmp;             //начинаем list со второй ячейки
        }
    }
    return true;
}
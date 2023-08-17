import math


def count_letters(text):
    return sum(1 for char in text if char.isalpha())


def count_words(text):
    return len(text.split())


def count_sentences(text):
    return text.count(".") + text.count("!") + text.count("?")


def main():
    text = input("Text: ")

    num_letters = count_letters(text)
    num_words = count_words(text)
    num_sentences = count_sentences(text)

    L = (num_letters / num_words) * 100
    S = (num_sentences / num_words) * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


if __name__ == "__main__":
    main()

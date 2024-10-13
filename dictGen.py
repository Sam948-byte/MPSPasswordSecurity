import calendar
import os
import nltk
from nltk.corpus import wordnet
from tqdm import tqdm


def generate_dates(start_year=2003, end_year=2024):
    """Generate dates in MM/DD/YY format between the given years."""
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                dates.append(f"{month:02}/{day:02}/{year % 100:02}")
    return dates


def generate_words():
    nltk.download("wordnet")

    words = list(wordnet.words())
    final_words = [word.title() for word in words if word.isalpha()]
    return final_words


if not os.path.exists("wordlists"):
    os.mkdir("wordlists")

if not os.path.isfile("wordlists/all.txt"):
    with open("wordlists/all.txt", "w") as file:
        words = generate_words()
        for word in tqdm(words, total=len(words)):
            file.write(word + "\n")

if not os.path.isfile("wordlists/4and5.txt"):
    with open("wordlists/4and5.txt", "w") as file:
        words = open("wordlists/all.txt").read().splitlines()
        final_words = [word for word in words if (len(word) == 4 or len(word) == 5)]
        for word in tqdm(final_words, total=len(final_words)):
            file.write(word + "\n")

if not os.path.isfile("wordlists/num4and5.txt"):
    with open("wordlists/num4and5.txt", "w") as file:
        words = open("wordlists/4and5.txt").read().splitlines()
        for num in range(100):
            for word in words:
                file.write(f"{word}{num:02}\n")

if not os.path.isfile("wordlists/dates.txt"):
    with open("wordlists/dates.txt", "w") as file:
        dates = generate_dates()
        for date in tqdm(dates, total=len(dates)):
            file.write(date + "\n")

print("Wordlists generated successfully.")

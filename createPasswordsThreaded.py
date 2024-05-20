import json
import random
import genhashes
import concurrent.futures
import calendar
from tqdm import tqdm


def generate_numbers():
    """ Generate a list of possible numbers in the format. """
    nums = (str(i) for i in range(0, 100))

    # Append a 0 to the front of each number if it is less than 10
    return [f"0{num}" if len(num) == 1 else num for num in nums]


def generate_words():
    with open("wordlists/wordnet4and5.txt") as f:
        words = f.read().splitlines()
    return words


def generate_dates(start_year=2000, end_year=2024):
    """ Generate dates in MM/DD/YY format between the given years. """
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                dates.append(f"{month:02}/{day:02}/{year % 100:02}")
    return dates

def create_passwords(numbers, words, dates):
    passwords = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create_password, number, word, date)
            for date in dates
            for word in words
            for number in numbers
        ]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Generating passwords"):
            passwords.append(future.result())
    return passwords

def create_password(number, word, date):
    return genhashes.main(f"{date}{word}{number}")

def create_random_password():
    dates = generate_dates()
    words = generate_words()
    numbers = generate_numbers()

    date = random.choice(dates)
    word = random.choice(words)
    number = random.choice(numbers)

    return genhashes.main(f"{date}{word}{number}")


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        numbers_future = executor.submit(generate_numbers)
        words_future = executor.submit(generate_words)
        dates_future = executor.submit(generate_dates)

        numbers = numbers_future.result()
        words = words_future.result()
        dates = dates_future.result()

        passwords = create_passwords(numbers, words, dates)

        with open('hashes/hashes4and5.json', 'w') as f:
            json.dump(passwords, f)


if __name__ == "__main__":
    main()

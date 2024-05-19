import time
import json
import genhashes

with open("wordlists/words4and5.txt") as f:
    words = f.read().splitlines()

def generate_numbers():
    """ Generate a list of possible numbers in the format. """
    return (str(i) for i in range(00, 100))

def generate_words():
    """ Generate all possible words of the given length, assuming the first letter is capitalized and the rest are not. """
    return (word for word in words)

def generate_dates(start_year=2000, end_year=2024):
    """ Generate dates in DD/MM/YY format between the given years. """
    dates = []
    for year in range(start_year, end_year + 1):
        for day in range(1, 32):
            for month in range(1, 13):
                try:
                    dates.append(f"{month:02}/{day:02}/{year % 100:02}")
                except ValueError:
                    continue
    return dates

def create_passwords():
    passwords = []
    dates = generate_dates()
    for date in dates:
        print("currently generating for data, " + date)
        words = generate_words()
        for word in words:
            numbers = generate_numbers()
            for number in numbers:
                candidate = f"{date}{word.title()}{number}"
                passwords.append(candidate)
    return passwords

def hash_passwords(passwords):
    return {password: genhashes.main(password) for password in passwords}

print(hash_passwords(create_passwords()))
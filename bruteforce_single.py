import itertools
import string
import time

print("Generating dictionary...")
with open("words.txt") as f:
    words = f.read().splitlines()
final_words = []
for word in words:
    if len(word) == 4 and word.isalpha():
        final_words.append(word)

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

# def generate_words(length):
#     """ Generate all possible words of the given length, assuming the first letter is capitalized and the rest are not. """
#     return ("".join(word) for word in itertools.product(string.ascii_lowercase, repeat=length))

def generate_words(length):
    """ Generate all possible words of the given length, assuming the first letter is capitalized and the rest are not. """
    return (word for word in final_words)

def generate_numbers():
    """ Generate a list of possible numbers in the format. """
    return (str(i) for i in range(00, 100))

def bruteforce(target_password):
    i = 0
    start = time.time()
    dates = generate_dates()
    for date in dates:
        words = generate_words(4)
        for word in words:
            numbers = generate_numbers()
            for number in numbers:
                candidate = f"{date}{word.title()}{number}"
                print(candidate)
                if candidate == target_password:
                    print(f"Password found: {candidate} - took {i} iterations and {time.time() - start:.2f} seconds")
                    return candidate
                i += 1
    print("Password not found")
    return None

target_password = "12/03/09Yarn70"
bruteforce(target_password)

import time
import json
import genhashes
import concurrent.futures


def generate_numbers():
    """ Generate a list of possible numbers in the format. """
    nums = (str(i) for i in range(00, 100))

    #append a 0 to the front of each number if it is less than 10
    return [f"0{num}" if len(num) == 1 else num for num in nums]

def generate_words():
    with open("wordlists/words4and5.txt") as f:
        words = f.read().splitlines()
    return words

def generate_dates(start_year=2024, end_year=2024):
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

# def create_passwords(numbers, words, dates):
#     passwords = []
#     for date in dates:
#         print(date)
#         for word in words:
#             for number in numbers:
#                 passwords.append(genhashes.main(f"{date}{word}{number}"))
#     return passwords

def create_passwords(numbers, words, dates):
    passwords = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for date in dates:
            for word in words:
                for number in numbers:
                    futures.append(executor.submit(create_password, number, word, date))
        for future in concurrent.futures.as_completed(futures):
            passwords.append(future.result())
    return passwords

def create_password(number, word, date):
    return genhashes.main(f"{date}{word}{number}")



def main():
    # print(generate_numbers)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        numbers_future = executor.submit(generate_numbers)
        words_future = executor.submit(generate_words)
        dates_future = executor.submit(generate_dates)

        numbers = numbers_future.result()
        words = words_future.result()
        dates = dates_future.result()

        passwords = create_passwords(numbers, words, dates)

        with open('passwords.json', 'w') as f:
            json.dump(passwords, f)

if __name__ == "__main__":
    main()
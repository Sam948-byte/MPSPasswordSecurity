import itertools
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

print("Generating dictionary...")
with open("wordlists/words.txt") as f:
    words = f.read().splitlines()
final_words = [word for word in words if len(word) == 4 and word.isalpha()]

def generate_dates(start_year=2008, end_year=2010):
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

def generate_words():
    """ Yield words from the final_words list. """
    for word in final_words:
        yield word

def generate_numbers():
    """ Yield numbers in the format. """
    for i in range(10, 100):
        yield str(i)

def bruteforce_worker(dates_chunk, target_password, found_event):
    """ Worker function to attempt password cracking for a chunk of dates. """
    for date in dates_chunk:
        if found_event.is_set():
            return None
        for word in generate_words():
            if found_event.is_set():
                return None
            for number in generate_numbers():
                candidate = f"{date}{word.title()}{number}"
                print(candidate)
                if candidate == target_password:
                    print(f"Password found: {candidate}")
                    found_event.set()
                    return candidate
    return None

def bruteforce(target_password):
    dates = generate_dates()
    chunk_size = len(dates) // 8  # Adjust the chunk size based on your CPU cores
    found_event = threading.Event()
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(bruteforce_worker, dates[i:i + chunk_size], target_password, found_event)
                   for i in range(0, len(dates), chunk_size)]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                return result
    print("Password not found")
    return None

target_password = "12/03/09Yarn70"
bruteforce(target_password)

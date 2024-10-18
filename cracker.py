import datetime
import os
import subprocess
import bcrypt
import nltk
from nltk.corpus import wordnet
from tqdm import tqdm
import hashlib
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

NUM_HASHES = 100
HASH_TYPE = 0
PASS_TYPE = 1
START_DATE = "2003-01-01"
END_DATE = "2024-01-01"

def generate_dates(end_date, start_date):
    #Generate dates between the given dates
    dates = []
    delta = start_date - end_date
    for i in range(delta.days + 1):
        date = start_date + datetime.timedelta(days=i)
        dates.append(date.strftime("%m/%d/%y"))
    return dates


def get_words():
    nltk.download("wordnet")

    words = list(wordnet.words())
    final_words = [word.title() for word in words if word.isalpha()]
    return final_words

def dictGen(start_date, end_date):
    if not os.path.exists("wordlists"):
        os.mkdir("wordlists")

    if not os.path.isfile("wordlists/all.txt"):
        with open("wordlists/all.txt", "w") as file:
            words = get_words()
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

    # If file does not exist or date range does not match
    if not os.path.isfile("wordlists/dates.txt"):
        with open("wordlists/dates.txt", "w") as file:
            dates = generate_dates(start_date, end_date)
            for date in tqdm(dates, total=len(dates)):
                file.write(date + "\n")
    else:
        with open("wordlists/dates.txt", "r") as file:
            dates = file.read().splitlines()
        if len(dates) == 0 or not (dates[0] == start_date.strftime("%m/%d/%y") and dates[-1] == end_date.strftime("%m/%d/%y")):
            with open("wordlists/dates.txt", "w") as file:
                dates = generate_dates(start_date, end_date)
                for date in tqdm(dates, total=len(dates)):
                    file.write(date + "\n")

    if not os.path.isfile("wordlists/combined4and5.txt"):
        with open("wordlists/combined4and5.txt", "w") as file:
            words = open("wordlists/4and5.txt").read().splitlines()
            dates = open("wordlists/dates.txt").read().splitlines()
            for word in words:
                for date in dates:
                    file.write(f"{word}{date}\n")
            

    print("Wordlists generated successfully.")

def generate_numbers():
    """ Generate a list of possible numbers in the format. """
    nums = (str(i) for i in range(0, 100))

    # Append a 0 to the front of each number if it is less than 10
    return [f"0{num}" if len(num) == 1 else num for num in nums]

def generate_words():
    with open("wordlists/4and5.txt") as f:
        words = f.read().splitlines()
    return words

def hash_password(password):

    password = password.encode('utf-8')    
    sha256_hash = hashlib.sha256(password).hexdigest()
    sha512_hash = hashlib.sha512(password).hexdigest()
    md5_hash    = hashlib.md5(password).hexdigest()
    shake_256   = hashlib.shake_256(password).hexdigest(64)
    sha3_256 = hashlib.sha3_256(password).hexdigest()
    sha3_512 = hashlib.sha3_512(password).hexdigest()
    bcrypt_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    #return dict of hashes
    return {
        'password': password.decode('utf-8'),
        '1400': sha256_hash,
        '1700': sha512_hash,
        '0': md5_hash,
        'shake_256': shake_256,
        '17400': sha3_256,
        '17600': sha3_512,
        '3200': bcrypt_hash
    }

def create_random_password(start_date, end_date, pass_type):
    dates = generate_dates(start_date, end_date)
    words = open("wordlists/4and5.txt").read().splitlines()
    numbers = generate_numbers()

    date = random.choice(dates)
    word = random.choice(words)
    number = random.choice(numbers)

    if pass_type == 1: 
        return hash_password(f"{date}{word}{number}") 
    elif pass_type == 2:
        return hash_password(f"{word}{number}")

def gen_randoms(num_hashes, start_date, end_date, pass_type):
    passwords = []

    with ThreadPoolExecutor() as executor:
        # Submit all tasks
        futures = [executor.submit(create_random_password, start_date, end_date, pass_type) for _ in range(num_hashes)]
        
        # Wait for tasks to complete and collect results
        for future in tqdm(as_completed(futures), total=num_hashes):
            passwords.append(future.result())

    with open("hashes/hashes.json", "w") as f:
        json.dump(passwords, f, indent=4)

def readFromJSON(type):
    # Read JSON data from a file
    with open('hashes/hashes.json', 'r') as file:
        data = json.load(file)

    # Extract sha512 hashes
    hashes = [entry[type] for entry in data]

    with open("hashes/hashes.txt", "w") as f:
        for hash in hashes:
            f.write(hash + "\n")

def solutionCheck(type):
    # Read JSON data from a file
    with open("hashes/hashes.json", "r") as file:
        data = json.load(file)

    with open("hashes/solution.txt", "r") as file:
        solution = file.read().splitlines()

    # Create a dictionary to store hash-password pairs
    hash_password_pairs = {}

    solution_pairs = {}

    # Populate the dictionary
    for entry in data:
        hash_value = entry[type]
        password = entry["password"]
        hash_password_pairs[hash_value] = password

    for entry in solution:
        if entry == "":
            continue
        hash_value, password = entry.split(":")
        solution_pairs[hash_value] = password

    allgood = True

    noMatches = 0

    # Verify the matching
    for hash_value, password in hash_password_pairs.items():
        if hash_value in solution_pairs:
            if password != solution_pairs[hash_value]:
                print(f"Hash value {hash_value} does not match")
                noMatches += 1
                allgood = False
        else:
            print(f"Hash value {hash_value} not found in the solution")
            noMatches += 1
            allgood = False

    if not allgood:
        print(f" {len(data) - noMatches}/{len(data)} hash values match.")
        raise Exception("Hash values do not match.")


def main(start_date, end_date, num_hashes, hash_type, pass_type):
    print("test")
    #parse dates
    start_date = datetime.date.fromisoformat(start_date)
    end_date = datetime.date.fromisoformat(end_date)


    # check for hashes directory and create if it doesn't exist
    if not os.path.exists("hashes"):
        os.makedirs("hashes")

    # generate wordlist
    dictGen(start_date, end_date)

    # clear files hashes.json, solution.txt and hashes.txt
    os.system("echo '' > hashes/hashes.json")
    os.system("echo '' > hashes/solution.txt")
    os.system("echo '' > hashes/hashes.txt")

    # generate hashes
    gen_randoms(num_hashes, start_date, end_date, pass_type)
    readFromJSON(str(hash_type))

    # crack hashes
    if pass_type == 1:
        subprocess.run(
            [
                "hashcat",
                "-m",
                str(hash_type),
                "-O",
                "-o",
                "hashes/solution.txt",
                "hashes/hashes.txt",
                "-a",
                "1",
                "wordlists/dates.txt",
                "wordlists/num4and5.txt",
                "-D",
                "1,2",
                "-w",
                "3",
            ]
        )
    #known date
    elif pass_type == 2:
        subprocess.run(
            [
                "hashcat",
                "-m",
                str(hash_type),
                "-O",
                "-o",
                "hashes/solution.txt",
                "hashes/hashes.txt",
                "-a",
                "6",
                "wordlists/4and5.txt",
                "?d?d",
                "-D",
                "1,2",
                "-w",
                "3",
            ]
        )

    # check solution
    solutionCheck(str(hash_type))


if __name__ == "__main__":
    main(START_DATE, END_DATE, NUM_HASHES, HASH_TYPE, PASS_TYPE)
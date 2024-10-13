import calendar
import sys
import os
import subprocess
import time
import bcrypt
import nltk
from nltk.corpus import wordnet
from tqdm import tqdm
import hashlib
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


def generate_dates(start_year=2003, end_year=2024):
    """Generate dates in MM/DD/YY format between the given years."""
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                dates.append(f"{month:02}/{day:02}/{year % 100:02}")
    return dates

def get_words():
    nltk.download("wordnet")

    words = list(wordnet.words())
    final_words = [word.title() for word in words if word.isalpha()]
    return final_words

def dictGen():
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

    if not os.path.isfile("wordlists/dates.txt"):
        with open("wordlists/dates.txt", "w") as file:
            dates = generate_dates()
            for date in tqdm(dates, total=len(dates)):
                file.write(date + "\n")

    print("Wordlists generated successfully.")

def print_usage():
    print(f"Usage: {sys.argv[0]} <hash num> <hash type> <pass type>")
    print("<number of hashes to generate> - number of hashes to generate")
    print("<type of hash> - type of hash to generate")
    print("    0 - MD5")
    print("    1400 - SHA-256")
    print("    1700 - SHA-512")
    print("    3200 - bcrypt")
    print("    17400 - SHA-3 (Keccak)")
    print("    17600 - SHA-3 (Keccak) - 512")
    print("<type of password> - type of password to generate")
    print("    1 - MPS")
    print("    2 - passphrase")
    print("call with -h for help")

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

def create_random_password():
    dates = generate_dates()
    words = generate_words()
    numbers = generate_numbers()

    date = random.choice(dates)
    word = random.choice(words)
    number = random.choice(numbers)

    return hash_password(f"{date}{word}{number}")

def gen_randoms(num_hashes):
    num_hashes = int(num_hashes)
    passwords = []

    with ThreadPoolExecutor() as executor:
        # Submit all tasks
        futures = [executor.submit(create_random_password) for _ in range(num_hashes)]
        
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


def main():
    # Check if the help flag is set
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print_usage()
        sys.exit(0)

    # Check if the number of arguments provided is correct
    if len(sys.argv) not in [2, 3, 4]:
        print_usage()
        sys.exit(1)

    # set hash type
    if len(sys.argv) not in [3, 4]:
        print("Type of hash not provided, defaulting to SHA-512")
        hash_type = 1700
    elif int(sys.argv[2]) not in [0, 1700, 1400, 17400, 17600, 3200]:
        print("Invalid hash type, defaulting to SHA-512")
        hash_type = 1700
    else:
        hash_type = int(sys.argv[2])

    if len(sys.argv) != 4:
        print("Type of password not provided, defaulting to MPS")
        pass_type = 1
    elif int(sys.argv[3]) not in [1, 2]:
        print("Invalid password type, defaulting to MPS")
        pass_type = 1
    elif int(sys.argv[3]) == 2:
        print("Passphrase not implemented, defaulting to MPS")
        pass_type = 1
    else:
        pass_type = int(sys.argv[3])

    # check for hashes directory and create if it doesn't exist
    if not os.path.exists("hashes"):
        os.makedirs("hashes")

    # generate wordlist
    dictGen()

    # clear files hashes.json, solution.txt and hashes.txt
    os.system("echo '' > hashes/hashes.json")
    os.system("echo '' > hashes/solution.txt")
    os.system("echo '' > hashes/hashes.txt")

    # generate hashes
    gen_randoms(sys.argv[1])
    readFromJSON(str(hash_type))

    start_time = time.time()

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
            ]
        )
    # elif pass_type == 2:
    #     subprocess.run(
    #         [
    #             "hashcat",
    #             "-m",
    #             str(hash_type),
    #             "-O",
    #             "-o",
    #             "hashes/solution.txt",
    #             "hashes/hashes.txt",
    #             "-a",
    #             "6",
    #             "wordlists/all.txt",
    #             "?w?w?w?w?w?w?w?w",
    #         ]
    #     )

    end_time = time.time()

    # check solution
    solutionCheck(str(hash_type))
    print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
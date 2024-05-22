import calendar
import hashlib
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import bcrypt
from tqdm import tqdm

def generate_numbers():
    """ Generate a list of possible numbers in the format. """
    nums = (str(i) for i in range(0, 100))

    # Append a 0 to the front of each number if it is less than 10
    return [f"0{num}" if len(num) == 1 else num for num in nums]


def generate_words():
    with open("wordlists/4and5.txt") as f:
        words = f.read().splitlines()
    return words


def generate_dates(start_year=2003, end_year=2024):
    """ Generate dates in MM/DD/YY format between the given years. """
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                dates.append(f"{month:02}/{day:02}/{year % 100:02}")
    return dates

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
        'bcrypt': bcrypt_hash
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

    with open("hashes/random.json", "w") as f:
        json.dump(passwords, f, indent=4)


if __name__ == "__main__":
    #check for command line argument
    if len(sys.argv) > 1:
        print("Generating random hashes...")
        gen_randoms(sys.argv[1])
    else:
        print("Please provide the number of hashes as a command line argument.")
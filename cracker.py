import datetime
import io
import os
import re
import selectors
import subprocess
import sys
import bcrypt
import nltk
from nltk.corpus import wordnet
from tqdm import tqdm
import hashlib
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

NUM_HASHES = 10
HASH_TYPE = "1710"
PASS_TYPE = 1
START_DATE = "2003-01-01"
END_DATE = "2024-01-01"


# Necessary for printing and capturing output at the same time
# Credit to https://gist.github.com/nawatts/e2cdca610463200c12eac2a14efc0bfb
def capture_subprocess_output(subprocess_args):
    # Start subprocess
    # bufsize = 1 means output is line buffered
    # universal_newlines = True is required for line buffering
    process = subprocess.Popen(
        subprocess_args,
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    # Create callback function for process output
    buf = io.StringIO()

    def handle_output(stream, mask):
        # Because the process' output is line buffered, there's only ever one
        # line to read when this function is called
        line = stream.readline()
        buf.write(line)
        sys.stdout.write(line)

    # Register callback for an "available for read" event from subprocess' stdout stream
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, handle_output)

    # Loop until subprocess is terminated
    while process.poll() is None:
        # Wait for events and handle them with their registered callbacks
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    # Ensure all remaining output is processed
    while True:
        line = process.stdout.readline()
        if not line:
            break
        buf.write(line)
        sys.stdout.write(line)

    # Get process return code
    return_code = process.wait()
    selector.close()

    success = return_code == 0

    # Store buffered output
    output = buf.getvalue()
    buf.close()

    return (success, output)


def add_to_json_file(file_path, new_data):
    try:
        # Load existing data
        with open(file_path, "r") as file:
            data = json.load(file)
            # Ensure data is a list to allow appending
            if not isinstance(data, list):
                data = [data]
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty, start with an empty list
        data = []

    # Append the new data as a new entry in the list
    data.append(new_data)

    # Write updated data back to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def generate_dates(start_date, end_date):
    # Generate dates between the given dates
    dates = []
    delta = end_date - start_date
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
        if len(dates) == 0 or not (
            dates[0] == start_date.strftime("%m/%d/%y")
            and dates[-1] == end_date.strftime("%m/%d/%y")
        ):
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
    """Generate a list of possible numbers in the format."""
    nums = (str(i) for i in range(0, 100))

    # Append a 0 to the front of each number if it is less than 10
    return [f"0{num}" if len(num) == 1 else num for num in nums]


def generate_words():
    with open("wordlists/4and5.txt") as f:
        words = f.read().splitlines()
    return words


def hash_password(password, hash_type):
    salt = os.urandom(16)  # Generate a random 16-byte salt
    password_bytes = password.encode("utf-8")

    # Create a dictionary to map hash types to their corresponding functions
    hash_dict = {
        "1400": lambda: hashlib.sha256(password_bytes).hexdigest(),
        "1410": lambda: hashlib.sha256(
            (password_bytes + salt.hex().encode("utf-8"))
        ).hexdigest()
        + ":"
        + salt.hex(),
        "1700": lambda: hashlib.sha512(password_bytes).hexdigest(),
        "1710": lambda: hashlib.sha512(
            (password_bytes + salt.hex().encode("utf-8"))
        ).hexdigest()
        + ":"
        + salt.hex(),
        "0": lambda: hashlib.md5(password_bytes).hexdigest(),
        "17400": lambda: hashlib.sha3_256(password_bytes).hexdigest(),
        # "17410": lambda: hashlib.sha3_256(salt + password_bytes).hexdigest() + ":" + salt.hex(),
        "17600": lambda: hashlib.sha3_512(password_bytes).hexdigest(),
        # "1711": lambda: hashlib.sha3_512(salt + password_bytes).hexdigest() + ":" + salt.hex(),
        "3200": lambda: bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8"),
    }

    # Return dict of hashes
    return {
        "password": password,
        "hash": hash_dict.get(hash_type, lambda: "Invalid hash type")(),
    }


def create_random_password(start_date, end_date, pass_type, hash_type):
    dates = generate_dates(start_date, end_date)
    words = open("wordlists/4and5.txt").read().splitlines()
    numbers = generate_numbers()

    date = random.choice(dates)
    word = random.choice(words)
    number = random.choice(numbers)

    if pass_type == 1:
        return hash_password(f"{date}{word}{number}", hash_type)
    elif pass_type == 2:
        return hash_password(f"{word}{number}", hash_type)


def gen_randoms(num_hashes, start_date, end_date, pass_type, hash_type):
    passwords = []

    with ThreadPoolExecutor() as executor:
        # Submit all tasks
        futures = [
            executor.submit(
                create_random_password, start_date, end_date, pass_type, hash_type
            )
            for _ in range(num_hashes)
        ]

        # Wait for tasks to complete and collect results
        for future in tqdm(as_completed(futures), total=num_hashes):
            passwords.append(future.result())

    with open("hashes/hashes.json", "w") as f:
        json.dump(passwords, f, indent=4)


def readFromJSON():
    # Read JSON data from a file
    with open("hashes/hashes.json", "r") as file:
        data = json.load(file)

    # Extract hashes
    hashes = [entry["hash"] for entry in data]

    with open("hashes/hashes.txt", "w") as f:
        for hash in hashes:
            f.write(hash + "\n")


def solutionCheck():
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
        hash_value = entry["hash"]
        password = entry["password"]
        hash_password_pairs[hash_value] = password

    for entry in solution:
        if entry == "":
            continue
        numColons = entry.count(":")
        if numColons == 2:
            hash_value, salt, password = entry.split(":")
            hash_value = hash_value + ":" + salt
        elif numColons == 1:
            hash_value, password = entry.split(":")
        else:
            raise Exception("Invalid solution format")
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
    # parse dates
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
    gen_randoms(num_hashes, start_date, end_date, pass_type, hash_type)
    readFromJSON()

    # crack hashes
    if pass_type == 1:
        result = capture_subprocess_output(
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
    # known date
    elif pass_type == 2:
        result = capture_subprocess_output(
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
    solutionCheck()

    print("All hashes match.")

    # get runtime for hashcat
    start_match = re.search(r"Started: (.+)", result[1])
    stop_match = re.search(r"Stopped: (.+)", result[1])

    if start_match and stop_match:
        start_time_str = start_match.group(1)
        stop_time_str = stop_match.group(1)

        # Parse the times
        time_format = "%a %b %d %H:%M:%S %Y"
        start_time = datetime.datetime.strptime(start_time_str, time_format)
        stop_time = datetime.datetime.strptime(stop_time_str, time_format)

        # Compute the elapsed time
        elapsed_time = stop_time - start_time
        elapsed_time = elapsed_time.total_seconds()
        print(f"Elapsed time: {elapsed_time}")
    else:
        print("Could not find start and/or stop time in output.")
        return 1

    dict = {
        "Hash Type": hash_type,
        "Pass Type": pass_type,
        "Number of Hashes": num_hashes,
        "Password Start Date": start_date.strftime("%m/%d/%y"),
        "Password End Date": end_date.strftime("%m/%d/%y"),
        "Elapsed Time": str(elapsed_time),
    }

    add_to_json_file("data/data.json", dict)


if __name__ == "__main__":
    main(START_DATE, END_DATE, NUM_HASHES, HASH_TYPE, PASS_TYPE)

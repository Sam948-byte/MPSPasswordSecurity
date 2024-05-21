import json
import sys

def main(type):
    # Read JSON data from a file
    with open('hashes/randomHashes.json', 'r') as file:
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

    # Verify the matching
    for hash_value, password in hash_password_pairs.items():
        if hash_value in solution_pairs:
            if password != solution_pairs[hash_value]:
                print(f"Hash value {hash_value} does not match")
                allgood = False
        else:
            print(f"Hash value {hash_value} not found in the solution")
            allgood = False

    if allgood:
        print("All hash values match!")

if __name__ == "__main__":
    #check for command line argument
    if len(sys.argv) > 1:
        print("Parsing hashes")
        main(sys.argv[1])
    else:
        print("Please provide the type of hash to parse.")
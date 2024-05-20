import json

# Read JSON data from a file
with open('hashes/random1000.json', 'r') as file:
    data = json.load(file)

with open("hashes/solution.txt", "r") as file:
    solution = file.read().splitlines()

# Create a dictionary to store hash-password pairs
hash_password_pairs = {}

solution_pairs = {}

# Populate the dictionary
for entry in data:
    hash_value = entry["sha512"]
    password = entry["password"]
    hash_password_pairs[hash_value] = password

for entry in solution:
    hash_value, password = entry.split(":")
    solution_pairs[hash_value] = password

# Verify the matching
for hash_value, password in hash_password_pairs.items():
    if hash_value in solution_pairs:
        if password != solution_pairs[hash_value]:
            print(f"Hash value {hash_value} does not match")
    else:
        print(f"Hash value {hash_value} not found in the solution")

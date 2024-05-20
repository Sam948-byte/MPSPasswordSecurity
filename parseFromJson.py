import json

# Read JSON data from a file
with open('hashes/random1000.json', 'r') as file:
    data = json.load(file)

# Extract sha512 hashes
sha512_hashes = [entry["sha512"] for entry in data]

with open("hashes/sha512.txt", "w") as f:
    for hash in sha512_hashes:
        f.write(hash + "\n")

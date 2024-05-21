import json
import sys

def main(type):
    # Read JSON data from a file
    with open('hashes/random.json', 'r') as file:
        data = json.load(file)

    # Extract sha512 hashes
    hashes = [entry[type] for entry in data]

    with open("hashes/hashes.txt", "w") as f:
        for hash in hashes:
            f.write(hash + "\n")

if __name__ == "__main__":
    #check for command line argument
    if len(sys.argv) > 1:
        print("Parsing hashes")
        main(sys.argv[1])
    else:
        print("Please provide the type of hash to parse.")
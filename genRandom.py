import json
import genPassAndHashes
import sys

def gen_randoms(num_hashes):
    passwords = []
    num_hashes = int(num_hashes)
    for i in range(num_hashes):
        print(i)
        passwords.append(genPassAndHashes.gen_pass_and_hashes())

    with open("hashes/randomHashes.json", "w") as f:
        json.dump(passwords, f, indent=4)

if __name__ == "__main__":
    #check for command line argument
    if len(sys.argv) > 1:
        gen_randoms(sys.argv[1])
    else:
        print("No argument provided to genRandom.")
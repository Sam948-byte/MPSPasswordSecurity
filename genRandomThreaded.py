import json
import genPassAndHashes
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def gen_randoms(num_hashes):
    num_hashes = int(num_hashes)
    passwords = []

    with ThreadPoolExecutor() as executor:
        # Submit all tasks
        futures = [executor.submit(genPassAndHashes.gen_pass_and_hashes) for _ in range(num_hashes)]
        
        # Wait for tasks to complete and collect results
        for future in tqdm(as_completed(futures), total=num_hashes):
            passwords.append(future.result())

    with open("hashes/randomHashes.json", "w") as f:
        json.dump(passwords, f, indent=4)


if __name__ == "__main__":
    #check for command line argument
    if len(sys.argv) > 1:
        gen_randoms(sys.argv[1])
    else:
        print("Please provide the number of hashes as a command line argument.")
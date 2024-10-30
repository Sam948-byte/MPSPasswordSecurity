from datetime import datetime
import os
import cracker 

ITERATIONS = 1
HASH_TYPES = { "0", "1400", "1700", "17600", "1410", "1710" }
NUM_HASHES = {1}
PASS_TYPE = 1
START_DATE = "2003-01-01"
END_DATE = "2024-01-01"

def main():
    if not os.path.exists("data/main.log"):
        os.system("touch data/main.log")

    with open("data/main.log", "a") as f:
        f.write("\nStarting main " + str(datetime.now()) + "\n")

    for hash in HASH_TYPES:
        for num in NUM_HASHES:
            with open("data/main.log", "a") as f:
                f.write(f"Starting hash {hash}, num {num}, iterations {ITERATIONS}\n")
            for i in range(0, ITERATIONS):
                try:
                    cracker.main(START_DATE, END_DATE, num, hash, PASS_TYPE)
                except Exception as e:
                    with open("data/main.log", "a") as f:
                        f.write(f"Error in cracker.main with hash {hash}, num {num}, iteration {i}: {e}\n")


if __name__ == "__main__":
    main()
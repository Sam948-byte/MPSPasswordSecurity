from datetime import datetime
import os
import cracker


def log(string):
    with open("data/main.log", "a") as f:
        f.write(string + "\n")


ITERATIONS = 10
HASH_TYPES_UNSALTED = {"0", "1400", "1700", "17600"}
HASH_TYPES_SALTED = {"1410", "1710"}
HASH_TYPES = {*HASH_TYPES_SALTED}
NUM_HASHES = {1, 1000}
PASS_TYPE = 1
START_DATE = "2003-01-01"
END_DATE = "2024-01-01"


def main():
    if not os.path.exists("data/main.log"):
        os.system("touch data/main.log")

    log(f"\nStarting main.py at {datetime.now()}")

    for hash in HASH_TYPES:
        for num in NUM_HASHES:
            log(
                f"Starting hash {hash}, num {num}, iterations {ITERATIONS} at {datetime.now()}"
            )
            for i in range(0, ITERATIONS):
                try:
                    cracker.main(START_DATE, END_DATE, num, hash, PASS_TYPE)
                except Exception as e:
                    log(
                        f"Error in cracker.main with hash {hash}, num {num}, iteration {i}: {e}\n"
                    )


if __name__ == "__main__":
    main()

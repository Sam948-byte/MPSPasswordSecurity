import cracker

ITERATIONS = 10
HASH_TYPES = { "0", "1400", "1700", "17600", "1410", "1710" }
NUM_HASHES = {1, 1000}
PASS_TYPE = 1
START_DATE = "2003-01-01"
END_DATE = "2024-01-01"

def main():
    for hash in HASH_TYPES:
        for num in NUM_HASHES:
            for i in range(0, ITERATIONS):
                cracker.main(START_DATE, END_DATE, num, hash, PASS_TYPE)

if __name__ == "__main__":
    main()
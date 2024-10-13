import sys
import os
import subprocess
import time


def print_usage():
    print(f"Usage: {sys.argv[0]} <hash num> <hash type> <pass type>")
    print("<number of hashes to generate> - number of hashes to generate")
    print("<type of hash> - type of hash to generate")
    print("    0 - MD5")
    print("    1400 - SHA-256")
    print("    1700 - SHA-512")
    print("    3200 - bcrypt")
    print("    17400 - SHA-3 (Keccak)")
    print("    17600 - SHA-3 (Keccak) - 512")
    print("<type of password> - type of password to generate")
    print("    1 - MPS")
    print("    2 - passphrase")
    print("call with -h for help")


def main():
    # Check if the help flag is set
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print_usage()
        sys.exit(0)

    # Check if the number of arguments provided is correct
    if len(sys.argv) not in [2, 3, 4]:
        print_usage()
        sys.exit(1)

    # set hash type
    if len(sys.argv) not in [3, 4]:
        print("Type of hash not provided, defaulting to SHA-512")
        hash_type = 1700
    elif int(sys.argv[2]) not in [0, 1700, 1400, 17400, 17600, 3200]:
        print("Invalid hash type, defaulting to SHA-512")
        hash_type = 1700
    else:
        hash_type = int(sys.argv[2])

    if len(sys.argv) != 4:
        print("Type of password not provided, defaulting to MPS")
        pass_type = 1
    elif int(sys.argv[3]) not in [1, 2]:
        print("Invalid password type, defaulting to MPS")
        pass_type = 1
    else:
        pass_type = int(sys.argv[3])

    # check for hashes directory and create if it doesn't exist
    if not os.path.exists("hashes"):
        os.makedirs("hashes")

    # check for worldlists directory and create if it doesn't exist
    if not os.path.exists("wordlists"):
        os.makedirs("wordlists")

    # generate wordlist
    os.system(f"python3 dictGen.py")

    # clear files hashes.json, solution.txt and hashes.txt
    os.system("echo '' > hashes/hashes.json")
    os.system("echo '' > hashes/solution.txt")
    os.system("echo '' > hashes/hashes.txt")

    # generate hashes
    os.system(f"python3 genThreaded.py {sys.argv[1]} {pass_type}")
    os.system(f"python3 parseFromJson.py {hash_type}")

    start_time = time.time()

    # crack hashes
    if pass_type == 1:
        subprocess.run(
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
            ]
        )
    # elif pass_type == 2:
    #     subprocess.run(
    #         [
    #             "hashcat",
    #             "-m",
    #             str(hash_type),
    #             "-O",
    #             "-o",
    #             "hashes/solution.txt",
    #             "hashes/hashes.txt",
    #             "-a",
    #             "6",
    #             "wordlists/all.txt",
    #             "?w?w?w?w?w?w?w?w",
    #         ]
    #     )

    end_time = time.time()

    # check solution
    os.system(f"python3 solutionCheck.py {hash_type}")
    print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
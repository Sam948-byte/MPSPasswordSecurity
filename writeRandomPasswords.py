import sys
import genPassAndHashes
import json

def gen(num):
    passwords = []
    for i in range(int(num)):
        print(f"Generating password {i+1} of {num}")
        password = genPassAndHashes.gen_pass_and_hashes()
        passwords.append(password)
    return passwords

if __name__ == "__main__":
    if len(sys.argv) > 2:
        num = sys.argv[1]
        out = sys.argv[2]
        passwords = gen(num)
        with open(out, 'w') as f:
            json.dump(passwords, f)
    else:
        print("No argument provided.")
        sys.exit(1)


    

import os
import sys
import subprocess
import re

hashes = [0, 1400, 1700, 3200, 17400, 17600]

def extract_time(output):
    # The regex pattern for the time
    pattern = r"Time taken: (\d+\.\d+) seconds"
    match = re.search(pattern, output)
    if match:
        return float(match.group(1))
    else:
        return None

for hash in hashes:
    #extract run time
    result = subprocess.run(["python3", "cracker.py", str(sys.argv[1]), str(hash), "1"], capture_output=True, text=True)
    time_taken = extract_time(result.stdout)
    print(f"Time taken for hash {hash} with pass type 1: {time_taken} seconds")

    #extract run time
    result = subprocess.run(["python3", "cracker.py", str(sys.argv[1]), str(hash), "2"], capture_output=True, text=True)
    time_taken = extract_time(result.stdout)
    print(f"Time taken for hash {hash} with pass type 2: {time_taken} seconds")
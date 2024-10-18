import subprocess
import re
from datetime import datetime

def main():
    result = subprocess.run(["/bin/python3", "/home/samf/gitClones/MPSPasswordSecurity/cracker.py"], capture_output=True, text=True, check=True)
    output = result.stdout.strip()
    # Extract the start and stop times using regular expressions
    start_match = re.search(r"Started: (.+)", output)
    stop_match = re.search(r"Stopped: (.+)", output)

    if start_match and stop_match:
        start_time_str = start_match.group(1)
        stop_time_str = stop_match.group(1)

        # Parse the times
        time_format = "%a %b %d %H:%M:%S %Y"
        start_time = datetime.strptime(start_time_str, time_format)
        stop_time = datetime.strptime(stop_time_str, time_format)

        # Compute the elapsed time
        elapsed_time = stop_time - start_time
        print(f"Elapsed time: {elapsed_time}")
    else:
        print("Could not find start and/or stop time in output.")

if __name__ == "__main__":
    main()
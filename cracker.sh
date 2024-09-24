#!/bin/bash

# Check if the number of arguments provided is correct
if [ $# -ne 1 ] && [ $# -ne 2 ]; then
    echo "Usage: $0 <number of hashes to generate> <type of hash>"
    exit 1
fi

# set hash type
if [ $# -ne 2 ]; then
    echo "Type of hash not provided, defaulting to SHA-512"
    HASHTYPE=1700
elif [ $2 -ne 0 ] && [ $2 -ne 1700 ] && [ $2 -ne 1400 ] && [ $2 -ne 17400 ] && [ $2 -ne 17600 ] && [ $2 -ne 3200 ]; then
    echo "Invalid hash type, defaulting to SHA-512"
    HASHTYPE=1700
else
    HASHTYPE=$2
fi

#check for hashes directory and create if it doesn't exist
if [ ! -d "hashes" ]; then
    mkdir hashes
fi

#check for wordlists directory and create if it doesn't exist
if [ ! -d "wordlists" ]; then
    mkdir wordlists
fi

# generate wordlist
python3 dictGen.py

# clear files
echo "" > hashes/random.json
echo "" > hashes/hashes.txt
echo "" > hashes/solution.txt

#generate hashes
python3 genRandomThreaded.py $1
python3 parseFromJson.py $HASHTYPE

#crack hashes
hashcat -m $HASHTYPE -O -o hashes/solution.txt hashes/hashes.txt -a 6 wordlists/combined.txt ?d?d

#check solution
python3 solutionCheck.py $HASHTYPE
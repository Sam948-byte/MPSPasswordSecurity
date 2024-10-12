#!/usr/bin/env bash

# Check if the help flag is set
if [ "$1" == "-h" ]; then
    echo "Usage: $0 <hash num> <hash type> <pass type>
    <number of hashes to generate> - number of hashes to generate
    <type of hash> - type of hash to generate
        0 - MD5
        1400 - SHA-256
        1700 - SHA-512
        3200 - bcrypt
        17400 - SHA-3 (Keccak)
        17600 - SHA-3 (Keccak) - 512
    <type of password> - type of password to generate
        1 - MPS
        2 - passphrase
    call with -h for help"
    exit 0
fi

# Check if the number of arguments provided is correct
if [ $# -ne 1 ] && [ $# -ne 2 ] && [ $# -ne 3 ]; then
    echo "Usage: $0  <hash num> <hash type> <pass type>
    call with -h for help"
    exit 1
fi

# set hash type
if [ $# -ne 2 ] && [ $# -ne 3 ]; then
    echo "Type of hash not provided, defaulting to SHA-512"
    HASHTYPE=1700
elif [ $2 -ne 0 ] && [ $2 -ne 1700 ] && [ $2 -ne 1400 ] && [ $2 -ne 17400 ] && [ $2 -ne 17600 ] && [ $2 -ne 3200 ]; then
    echo "Invalid hash type, defaulting to SHA-512"
    HASHTYPE=1700
else
    HASHTYPE=$2
fi

if [ $# -ne 3 ]; then
    echo "Type of password not provided, defaulting to MPS"
    PASSTYPE=1
elif [ $3 -ne 1 ] && [ $3 -ne 2 ]; then
    echo "Invalid password type, defaulting to MPS"
    PASSTYPE=1
else
    PASSTYPE=$3
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
echo "" > hashes/hashes.json
echo "" > hashes/hashes.txt
echo "" > hashes/solution.txt

#generate hashes
python3 genThreaded.py $1 $PASSTYPE
python3 parseFromJson.py $HASHTYPE

#crack hashes
if [ $PASSTYPE -eq 1 ]; then
    hashcat -m $HASHTYPE -O -o hashes/solution.txt hashes/hashes.txt -a 6 wordlists/combined4and5.txt ?d?d
elif [ $PASSTYPE -eq 2 ] ; then
    hashcat -m $HASHTYPE -O -o hashes/solution.txt hashes/hashes.txt -a 6 wordlists/all.txt ?w?w?w?w?w?w?w?w
fi

#check solution
python3 solutionCheck.py $HASHTYPE
#!/bin/bash

PASSWORDANDHASHES=$(python3 genPassAndHashes.py)

PASSWORD=$(echo $PASSWORDANDHASHES | cut -d ' ' -f 1)

SHA256HASH=$(echo $PASSWORDANDHASHES | cut -d ' ' -f 2)

SHA512HASH=$(echo $PASSWORDANDHASHES | cut -d ' ' -f 3)

MD5HASH=$(echo $PASSWORDANDHASHES | cut -d ' ' -f 4)

SHAKEHASH=$(echo $PASSWORDANDHASHES | cut -d ' ' -f 5)

BCRYPTHASH=$(echo $PASSWORDANDHASHES | cut -d ' ' -f 6)

echo "Password and Hashes Generated:"

echo "Password: $PASSWORD"

echo "SHA256 Hash: $SHA256HASH"

echo "SHA512 Hash: $SHA512HASH"

echo "MD5 Hash: $MD5HASH"

echo "SHAKE Hash: $SHAKEHASH"

echo "BCRYPT Hash: $BCRYPTHASH"
import argparse
import hashlib 
import bcrypt

def main():
    parser = argparse.ArgumentParser(description='Generate hashes for a password')
    parser.add_argument('password', type=str, help='Password to hash')
    args = parser.parse_args()

    password    = args.password.encode('utf-8')
    sha256_hash = hashlib.sha256(password).hexdigest()
    sha512_hash = hashlib.sha512(password).hexdigest()
    md5_hash    = hashlib.md5(password).hexdigest()
    shake_256   = hashlib.shake_256(password).hexdigest(64)
    bcrypt_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    print(f'SHA-256: {sha256_hash}')
    print(f'BCrypt: {bcrypt_hash}')
    print(f'SHA-512: {sha512_hash}')
    print(f'MD5: {md5_hash}')
    print(f'SHAKE-256: {shake_256}')

if __name__ == '__main__':
    main()
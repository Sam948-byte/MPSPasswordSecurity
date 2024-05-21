import hashlib 
import bcrypt

def main(password):

    password = password.encode('utf-8')    
    sha256_hash = hashlib.sha256(password).hexdigest()
    sha512_hash = hashlib.sha512(password).hexdigest()
    md5_hash    = hashlib.md5(password).hexdigest()
    shake_256   = hashlib.shake_256(password).hexdigest(64)
    bcrypt_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    #return dict of hashes
    return {
        'password': password.decode('utf-8'),
        '1400': sha256_hash,
        '1700': sha512_hash,
        '0': md5_hash,
        'shake_256': shake_256,
        'bcrypt': bcrypt_hash
    }

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate hashes for a password')
    parser.add_argument('password', type=str, help='Password to hash')
    args = parser.parse_args()
    main(args.password)
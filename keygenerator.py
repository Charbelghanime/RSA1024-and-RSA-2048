import millerrabin as mr
import math_1 as ma
import random

def keygenerated(keysize, public_key_file='public_key.txt', private_key_n_file='private_key_n.txt', private_key_d_file='private_key_d.txt'):
    print("Generating prime p...")
    p = mr.generateLargePrime(keysize)
    print("Generating prime q...")
    q = mr.generateLargePrime(keysize)
    n = p * q
    m = (p - 1) * (q - 1)
    
    print("Generating e that is relatively prime to (p-1)*(q-1)...")
    while True:
        e = random.randrange(2**(keysize-1), 2**(keysize))
        if ma.computeGCD(e, m) == 1:
            break
    
    print("Calculating d that is mod inverse of e...")
    d = ma.findModInverse(e, m)
    
    public_key = (n, e)
    
    # Writing public key to a file
    with open(public_key_file, 'w') as public_file:
        public_file.write(f"Public Key (n, e):\n{n}\n{e}")
    
    # Writing private key parts to separate files
    with open(private_key_n_file, 'w') as private_n_file:
        private_n_file.write(f"Private Key (n):\n{n}")
        
    with open(private_key_d_file, 'w') as private_d_file:
        private_d_file.write(f"Private Key (d):\n{d}")
    
    return public_key, (n, d)


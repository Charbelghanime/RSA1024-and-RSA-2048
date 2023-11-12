import millerrabin as mr
import math_1 as ma
import random
def keygenerated(keysize):
    print("Generating prime p...")
    p=mr.generateLargePrime(keysize)
    print("Generating prime q...")
    q=mr.generateLargePrime(keysize)
    n=p*q
    m=(p-1)*(q-1)
    print("Generating e that is relatively prime to (p-1)*(q-1)...")
    while True:
        e=random.randrange(2**(keysize-1),2**(keysize))
        if ma.computeGCD(e,m)==1:
            break
    print("Calculating d that is mod inverse of e...")
    d=ma.findModInverse(e,m)
    publickey=(n,e)
    privatekey=(n,d)
    return (publickey,privatekey)
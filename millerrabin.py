import random
def miller_rabin(n, k=10): # the goal here is to test if a number is prime or not. By doing this test 10 times we get a probability of 1-4^10 that this number is prime if it returns true. But we will still check if the number is prime by doing a primality test.

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1: #if we get x=1 or x=n-1 then this number satisfies the propertty 1 in the lecture.
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: #keep trying if we find x=n-1 as mentioned by property 2 in the lecture.
                break
        else:
            return False
    return True

def primalityTest(n):
   if (n < 2):
      return False
   lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
   67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
   157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 
   251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,317, 331, 337, 347, 349, 
   353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 
   457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 
   571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 
   673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
   797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 
   911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997] # low primes under 1000 to test wether this number is prime or not. We know that a number is composite if it can be written as a product of prime numbers.
   if n in lowPrimes:
        return True
   for prime in lowPrimes:
      if (n % prime == 0):
         return False
   return miller_rabin(n) #if the number is not divisible by any of the primes in the list then we do the miller rabin test
def generateLargePrime(keysize ):
   while True:
      num = random.randrange(2**(keysize-1), 2**(keysize))
      if primalityTest(num):
         return num
def computeGCD(x, y): #eucledean algorithm to find the gcd of two numbers. 
    while(y):
       x, y = y, x % y
    return abs(x)
def findModInverse(a, m):
   if computeGCD(a, m) != 1:
      return None
   u1, u2, u3 = 1, 0, a
   v1, v2, v3 = 0, 1, m
   
   while v3 != 0:
      q = u3 // v3
      v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
   return u1 % m #the typical table that we have used in the lecture to find the mod inverse.
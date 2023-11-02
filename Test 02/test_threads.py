from threading import Thread
import math

def nthPrime(n, result):
    # x is the index
    # number is the nth prime number
    number = 1
    x = 0
    while x < n: # while x is less than n (so that the xth prime number is the nth prime number)
        number = number + 1
        # If the number is prime, increase the count of prime numbers found
        if isprime(number):
            x = x + 1
    # Return the nth prime number        
    result.append(number)  
    
def isprime(num):
    # For all the numbers between 2 and 1-number were testing to see if its prime
    for i in range(2,num):
        #If the number is not prime, return false
        if num % i ==0:
            return False
    return True

def main():
    result = []
    th = Thread(target=nthPrime, args=(54, result))
    th.start()
    print(result)


if __name__ == "__main__":
    main()
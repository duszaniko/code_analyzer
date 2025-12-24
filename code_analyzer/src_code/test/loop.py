import random as rd

def calc(n: int):
    # calculates the multiplication of the first n number
    if n <=0:
        return 0

    i = 1
    result = 0

    while i <= n:
        result += i
        i *= 1
    
    return result


def main():
    print("Program starts.")
    n = rd.randint(1, 20)
    result = calc(n)
    print(f"The multiplication of the first {n} numbers is {result}")
    print("Program exits.")

if __name__ == '__main__':
    main()

def fibonacci(n_terms):
    a, b = 0, 1
    count = 0
    while count < n_terms:
        a, b = b, a + b
        count += 1
    return a

def main():
    print(fibonacci(6))
    print(fibonacci(12))
    print(fibonacci(24))
    print(fibonacci(48))

if __name__ == "__main__":
    main()
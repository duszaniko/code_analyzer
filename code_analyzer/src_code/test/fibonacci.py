def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    print(fibonacci(6))
    print(fibonacci(12))
    print(fibonacci(24))
    print(fibonacci(48))

if __name__ == "__main__":
    main()
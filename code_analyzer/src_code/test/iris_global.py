from sklearn.datasets import load_iris
import pandas as pd
import random as rd

IRIS = []

def load_iris_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    IRIS.append(df)

def main():
    ntimes = rd.randint(1, 5)
    print(f"Loop for {ntimes}.")
    i = 0
    while True:
        print(f"{i}. load.")
        load_iris_data()
        i += 2
        if i == ntimes:
            break

if __name__ == "__main__":
    main()
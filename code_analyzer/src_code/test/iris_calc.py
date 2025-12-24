from sklearn.datasets import load_iris
import pandas as pd

def load_datasets():
    iris = load_iris()
    iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_df["Target"] = iris.target
    iris_df['Species'] = iris_df['Target'].replace(to_replace= [0, 1, 2], value = iris['target_names'])
    return iris_df



def main():
    iris_df = load_datasets()
    iris_avg = iris_df.drop(columns=["Target"]).groupby("Species").mean()
    normal_columns = iris_avg.columns
    iris_avg.columns = ["Avg " + i  for i in iris_avg.columns]
    avg_columns = iris_avg.columns
    iris_avg = iris_avg.reset_index(drop=False)
    iris_df = iris_df.merge(iris_avg)

    all = pd.DataFrame()

    for i in range(0, len(iris_avg)+1):
        low = iris_df[iris_df[normal_columns[i]]  < iris_df[avg_columns[i]]]
        high = iris_df[iris_df[normal_columns[i]]  > iris_df[avg_columns[i]]]
        experiment = pd.concat([ low, high], ignore_index=False)
        experiment["Experiment"] = normal_columns[i]
        all = pd.concat([all, experiment], ignore_index=False)
    
    all_dropped = all.drop(columns=avg_columns)
    print(all_dropped.describe())

if __name__ == '__main__':
    main()
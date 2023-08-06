import pandas as pd
from sklearn.model_selection import train_test_split


def read(csv):
    return pd.read_csv(csv)

def split(df):
    X = df.iloc[:,:-1]
    y = df.iloc[:,-1:]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)
    return [X_train, X_test, y_train, y_test]



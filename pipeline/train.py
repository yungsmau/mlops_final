import pandas as pd
import joblib
import argparse
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def load_data(path):
    df = pd.read_csv(path)
    X = df.drop(columns=["y"])  # замените 'target' на вашу целевую переменную
    y = df["y"]
    return X, y


def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to CSV data")
    parser.add_argument("--output", required=True, help="Path to save model")
    args = parser.parse_args()

    X, y = load_data(args.data)
    model = train_model(X, y)
    joblib.dump(model, args.output)
    print(f"Model trained and saved to {args.output}")


if __name__ == "__main__":
    main()

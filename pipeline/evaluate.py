import pandas as pd
import joblib
import argparse
import json
from sklearn.metrics import mean_squared_error, r2_score


def load_data(path):
    df = pd.read_csv(path)
    X = df.drop(columns=["target"])  # замените 'target' на вашу целевую переменную
    y = df["target"]
    return X, y


def load_model(path):
    return joblib.load(path)


def evaluate(model, X, y):
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return mse, r2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--data", required=True, help="Path to CSV data")
    parser.add_argument("--metrics", required=True, help="Path to save metrics")
    args = parser.parse_args()

    model = load_model(args.model)
    X, y = load_data(args.data)
    mse, r2 = evaluate(model, X, y)

    metrics = {"mse": mse, "r2": r2}
    with open(args.metrics, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {args.metrics}: MSE={mse:.4f}, R2={r2:.4f}")


if __name__ == "__main__":
    main()

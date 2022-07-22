import pickle
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

ROOT = Path(__file__).parents[0]
MODEL_PATH = ROOT / "lr_model.pkl"
MODEL = []


def load_lr_model():
    model = pickle.load(open(MODEL_PATH.as_posix(), "rb"))
    return model


try:
    MODEL = load_lr_model()
except FileNotFoundError as fe:
    pass


def train_lr_model():

    data = pd.read_csv(ROOT / "expenses_prediction.csv")

    data.shape

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    df = pd.DataFrame.from_records(data_scaled)
    X = df.iloc[:, :2]
    Y = df.iloc[:, -1]
    lr_model = LinearRegression()
    lr_model.fit(X, Y)

    Y_predict = lr_model.predict(X)
    r2 = r2_score(Y, Y_predict)
    print("R2 score is {}".format(r2))
    # Saving model to disk
    pickle.dump(lr_model, open(MODEL_PATH.as_posix(), "wb"))


def predict_lr_model(features):
    global MODEL
    if not MODEL:
        train_lr_model()
        MODEL = load_lr_model()
    prediction = MODEL.predict(features)
    return prediction

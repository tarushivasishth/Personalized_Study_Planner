import joblib
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("saved_model/model.keras", compile=False)
scaler_x = joblib.load("saved_model/scaler_x.pkl")
scaler_y = joblib.load("saved_model/scaler_y.pkl")

levels = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3
}

def predict_time(deadline, difficulty, prev_score):
    difficulty = levels[difficulty]

    X = np.array([[deadline, difficulty, prev_score]])

    X[:, [0,2]] = scaler_x.transform(X[:, [0,2]])

    pred_time = model.predict(X)
    pred_time = scaler_y.inverse_transform(pred_time.reshape(-1, 1)).astype(int)

    return pred_time[0][0]
import joblib


def predict_room(time_of_day, task_type, room_status):

    bundle = joblib.load(
        "/home/saket/roboai_ws/room_classifier.pkl"
    )

    model = bundle["model"]

    x = [[
        bundle["time_encoder"].transform([time_of_day])[0],
        bundle["task_encoder"].transform([task_type])[0],
        bundle["status_encoder"].transform([room_status])[0]
    ]]

    prediction = model.predict(x)[0]

    room = bundle["room_encoder"].inverse_transform(
        [prediction]
    )[0]

    return room
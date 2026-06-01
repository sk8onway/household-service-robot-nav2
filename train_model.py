import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# Load dataset
df = pd.read_excel("project_dataset.xlsx")

# Encoders
time_encoder = LabelEncoder()
task_encoder = LabelEncoder()
status_encoder = LabelEncoder()
room_encoder = LabelEncoder()

# Encode features
df["Time of Day"] = time_encoder.fit_transform(df["Time of Day"])
df["Task Type"] = task_encoder.fit_transform(df["Task Type"])
df["Room status"] = status_encoder.fit_transform(df["Room status"])

# Encode target
y = room_encoder.fit_transform(df["Target Room"])

# Features
X = df[["Time of Day", "Task Type", "Room status"]]

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Save everything
joblib.dump(
    {
        "model": model,
        "time_encoder": time_encoder,
        "task_encoder": task_encoder,
        "status_encoder": status_encoder,
        "room_encoder": room_encoder,
    },
    "room_classifier.pkl",
)

print("Model trained and saved.")
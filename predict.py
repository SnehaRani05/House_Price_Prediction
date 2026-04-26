import pickle
import numpy as np
import sqlite3

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

feature_names = [
    "CRIM","ZN","INDUS","CHAS","NOX","RM","AGE",
    "DIS","RAD","TAX","PTRATIO","B","LSTAT"
]
# CRIM → crime rate (small number like 0.1, 0.5)
# ZN → land % (0–100)
# INDUS → industrial area (0–30 approx)
# CHAS → only 0 or 1
# NOX → pollution (0.3–0.8)
# RM → rooms (3–8 usually)
# AGE → % old houses (0–100)
# DIS → distance (1–10)
# RAD → index (1–24)
# TAX → tax (200–700)
# PTRATIO → 12–22
# B → ~300–400
# LSTAT → 1–40

print("\nEnter all feature values separated by space:")
print(feature_names)

while True:
    try:
        user_input = input("\nInput: ").strip().split()

        if len(user_input) != len(feature_names):
            print(f"Please enter exactly {len(feature_names)} values.")
            continue

        values = list(map(float, user_input))
        break

    except ValueError:
        print("Invalid input. Please enter only numbers.")

# Convert to numpy array
input_data = np.array([values])

prediction = model.predict(input_data)[0]

print(f"\nPredicted House Price: ${prediction:.2f}")

#saving in database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    CRIM REAL, ZN REAL, INDUS REAL, CHAS REAL,
    NOX REAL, RM REAL, AGE REAL, DIS REAL,
    RAD REAL, TAX REAL, PTRATIO REAL, B REAL,
    LSTAT REAL,
    predicted_price REAL
)
""")

# Insert data
cursor.execute("""
INSERT INTO prediction_logs (
    CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS,
    RAD, TAX, PTRATIO, B, LSTAT, predicted_price
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (*values, prediction))

conn.commit()
conn.close()

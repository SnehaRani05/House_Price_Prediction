import pandas as pd
import sqlite3

column_names = [
    "CRIM","ZN","INDUS","CHAS","NOX","RM","AGE",
    "DIS","RAD","TAX","PTRATIO","B","LSTAT","MEDV"
]

df = pd.read_csv("housing.csv", sep="\s+", names=column_names)

print("Shape:", df.shape)

# Connect to SQLite
conn = sqlite3.connect("database.db")

# Store in SQL
df.to_sql("housing_data", conn, if_exists="replace", index=False)

conn.close()

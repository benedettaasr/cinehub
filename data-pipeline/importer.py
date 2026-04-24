import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv("../.env")

print("Connection to database...")
conn = psycopg2.connect(os.getenv("DB_URL"))
cursor = conn.cursor()
print("Connected!")

# Loading CSV
watched = pd.read_csv("../data/watched.csv")
diary = pd.read_csv("../data/diary.csv")

# Join the dataframe on movie name and year

movies = pd.merge(watched, diary[["Name", "Year", "Letterboxd URI", "Rating", "Rewatch", "Watched Date"]], on=["Name", "Year"], how="left", suffixes=("_watched", "_diary"))

# Substitute empty values with None

movies = movies.where(pd.notna(movies), None)

# Insert on database

for _, row in movies.iterrows():
    cursor.execute("""
        INSERT INTO Movies (Name, Year, LetterboxdURI, Rating, Rewatch, WatchedDate)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (LetterboxdURI) DO NOTHING
    """, (
        row["Name"],
        row["Year"],
        row["Letterboxd URI_watched"],
        row["Rating"] if pd.notna(row["Rating"]) else None,
        row["Rewatch"] == "Yes" if pd.notna(row["Rewatch"]) else None,
        row["Watched Date"] if pd.notna(row["Watched Date"]) else None,
    ))

conn.commit()
cursor.close()
conn.close()

print(f"Imported {len(movies)} movies!")
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('game.db')

# Create a table for cities
conn.execute('''
CREATE TABLE IF NOT EXISTS Cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);
''')

# Create a table for clues
conn.execute('''
CREATE TABLE IF NOT EXISTS Clues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER,
    clue_type TEXT NOT NULL,
    clue_content TEXT NOT NULL,
    FOREIGN KEY(city_id) REFERENCES Cities(id)
);
''')

# Insert sample cities and clues
conn.execute("INSERT INTO Cities (name, latitude, longitude) VALUES ('New York', 40.7128, -74.0060);")
conn.execute("INSERT INTO Cities (name, latitude, longitude) VALUES ('London', 51.5074, -0.1278);")
conn.execute("INSERT INTO Cities (name, latitude, longitude) VALUES ('Tokyo', 35.6895, 139.6917);")

conn.execute("INSERT INTO Clues (city_id, clue_type, clue_content) VALUES (1, 'Landmark', 'Statue of Liberty');")
conn.execute("INSERT INTO Clues (city_id, clue_type, clue_content) VALUES (2, 'Landmark', 'Big Ben');")
conn.execute("INSERT INTO Clues (city_id, clue_type, clue_content) VALUES (3, 'Landmark', 'Mount Fuji visible');")

# Commit changes and close connection
conn.commit()
conn.close()


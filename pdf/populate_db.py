import sqlite3
import random

def populate_database(db_name="ships.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for i in range(1, 21):
        c.execute("INSERT INTO weapons VALUES (?, ?, ?, ?, ?, ?)", (
            f"weapon-{i}",
            random.randint(1, 20),
            random.randint(1, 20),
            random.randint(1, 20),
            random.randint(1, 20),
            random.randint(1, 20)
        ))

    for i in range(1, 6):
        c.execute("INSERT INTO hulls VALUES (?, ?, ?, ?)", (
            f"hull-{i}",
            random.randint(1, 20),
            random.randint(1, 20),
            random.randint(1, 20)
        ))

    for i in range(1, 7):
        c.execute("INSERT INTO engines VALUES (?, ?, ?)", (
            f"engine-{i}",
            random.randint(1, 20),
            random.randint(1, 20)
        ))

    for i in range(1, 201):
        c.execute("INSERT INTO ships VALUES (?, ?, ?, ?)", (
            f"ship-{i}",
            f"weapon-{random.randint(1, 20)}",
            f"hull-{random.randint(1, 5)}",
            f"engine-{random.randint(1, 6)}"
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_database()

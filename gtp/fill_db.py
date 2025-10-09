import sqlite3
import random

conn = sqlite3.connect(".db")  # -- вынести название ДБ в переменную
cursor = conn.cursor()


# в задании сказано, что все интежеры от 1 до 20 то решил функцию для этого создать
def rand_for_integer():
    return random.randint(1, 20)


weapons_quantity = 20
hulls_quantity = 5
engines_quantity = 6
ships_quantity = 200

# for i in range(weapons_quantity):
#     cursor.execute("""
#         INSERT INTO weapons (weapon, reload_speed, rotational_speed, diameter, power_volley, count)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         f"Weapon-{i + 1}", rand_for_integer(), rand_for_integer(), rand_for_integer(), rand_for_integer(),
#         rand_for_integer()))
#
# for i in range(hulls_quantity):
#     cursor.execute("""
#         INSERT INTO hulls (hull, armor, type, capacity)
#         VALUES (?, ?, ?, ?)
#     """, (f"Hull-{i + 1}", rand_for_integer(), rand_for_integer(), rand_for_integer()))


# Генерация данных для weapons
weapons_data = [
    (
        f"Weapon-{i + 1}",
        rand_for_integer(),
        rand_for_integer(),
        rand_for_integer(),
        rand_for_integer(),
        rand_for_integer()
    )
    for i in range(weapons_quantity)
]

# Генерация данных для hulls
hulls_data = [
    (
        f"Hull-{i + 1}",
        rand_for_integer(),
        rand_for_integer(),
        rand_for_integer()
    )
    for i in range(hulls_quantity)
]

# Вставка в одной транзакции
cursor.execute("BEGIN TRANSACTION")

cursor.executemany("""
    INSERT INTO weapons (weapon, reload_speed, rotational_speed, diameter, power_volley, count)
    VALUES (?, ?, ?, ?, ?, ?)
""", weapons_data)

cursor.executemany("""
    INSERT INTO hulls (hull, armor, type, capacity)
    VALUES (?, ?, ?, ?)
""", hulls_data)

cursor.execute("COMMIT")

# for i in range(engines_quantity):
#     cursor.execute("""
#         INSERT INTO engines (engine, power, type)
#         VALUES (?, ?, ?)
#     """, (f"Engine-{i + 1}", rand_for_integer(), rand_for_integer()))

data = [
    (f"Engine-{i + 1}", rand_for_integer(), rand_for_integer())
    for i in range(engines_quantity)
]
cursor.executemany("""
    INSERT INTO engines (engine, power, type)
    VALUES (?, ?, ?)
""", data)

# for i in range(ships_quantity):
#     weapon = f"Weapon-{random.randint(1, weapons_quantity)}"
#     hull = f"Hull-{random.randint(1, hulls_quantity)}"
#     engine = f"Engine-{random.randint(1, engines_quantity)}"
#     cursor.execute("""
#         INSERT INTO ships (ship, weapon, hull, engine)
#         VALUES (?, ?, ?, ?)
#     """, (f"Ship-{i + 1}", weapon, hull, engine))


ships_data = [
    (
        f"Ship-{i + 1}",
        f"Weapon-{random.randint(1, weapons_quantity)}",
        f"Hull-{random.randint(1, hulls_quantity)}",
        f"Engine-{random.randint(1, engines_quantity)}"
    )
    for i in range(ships_quantity)
]

# Оборачиваем вставку в транзакцию
cursor.execute("BEGIN TRANSACTION")
cursor.executemany("""
    INSERT INTO ships (ship, weapon, hull, engine)
    VALUES (?, ?, ?, ?)
""", ships_data)
cursor.execute("COMMIT")

conn.commit()
conn.close()

# print("Database populated successfully.")

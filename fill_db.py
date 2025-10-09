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

hulls_data = [
    (
        f"Hull-{i + 1}",
        rand_for_integer(),
        rand_for_integer(),
        rand_for_integer()
    )
    for i in range(hulls_quantity)
]

data = [
    (
        f"Engine-{i + 1}",
        rand_for_integer(),
        rand_for_integer()
    )
    for i in range(engines_quantity)
]
ships_data = [
    (
        f"Ship-{i + 1}",
        f"Weapon-{random.randint(1, weapons_quantity)}",
        f"Hull-{random.randint(1, hulls_quantity)}",
        f"Engine-{random.randint(1, engines_quantity)}"
    )
    for i in range(ships_quantity)
]


conn.close()

# print("Database populated successfully.")

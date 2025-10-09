import sqlite3
import random

# Константы для конфигурации
DB_NAME = "database.db"
WEAPONS_COUNT = 20
HULLS_COUNT = 5
ENGINES_COUNT = 6
SHIPS_COUNT = 200
RANDOM_RANGE = (1, 20)


def get_random_integer():
    """Возвращает случайное целое число в заданном диапазоне."""
    return random.randint(*RANDOM_RANGE)


def generate_weapons_data():
    """Генерирует данные для таблицы weapons."""
    return [
        (
            f"Weapon-{i + 1}",
            get_random_integer(),
            get_random_integer(),
            get_random_integer(),
            get_random_integer(),
            get_random_integer()
        )
        for i in range(WEAPONS_COUNT)
    ]


def generate_hulls_data():
    """Генерирует данные для таблицы hulls."""
    return [
        (
            f"Hull-{i + 1}",
            get_random_integer(),
            get_random_integer(),
            get_random_integer()
        )
        for i in range(HULLS_COUNT)
    ]


def generate_engines_data():
    """Генерирует данные для таблицы engines."""
    return [
        (
            f"Engine-{i + 1}",
            get_random_integer(),
            get_random_integer()
        )
        for i in range(ENGINES_COUNT)
    ]


def generate_ships_data():
    """Генерирует данные для таблицы ships."""
    return [
        (
            f"Ship-{i + 1}",
            f"Weapon-{random.randint(1, WEAPONS_COUNT)}",
            f"Hull-{random.randint(1, HULLS_COUNT)}",
            f"Engine-{random.randint(1, ENGINES_COUNT)}"
        )
        for i in range(SHIPS_COUNT)
    ]


# def main():
def fill_db():
    # Подключение к базе данных
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # # Вставка данных в таблицу weapons
        # cursor.executemany("""
        #     INSERT INTO weapons (weapon, reload_speed, rotational_speed, diameter, power_volley, count)
        #     VALUES (?, ?, ?, ?, ?, ?)
        # """, generate_weapons_data())

        # Вставка данных в таблицу weapons
        sql = """
            INSERT INTO weapons (weapon, reload_speed, rotational_speed, diameter, power_volley, count)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(sql, generate_weapons_data())

        # Вставка данных в таблицу hulls
        cursor.executemany("""
            INSERT INTO hulls (hull, armor, type, capacity)
            VALUES (?, ?, ?, ?)
        """, generate_hulls_data())

        # Вставка данных в таблицу engines
        cursor.executemany("""
            INSERT INTO engines (engine, power, type)
            VALUES (?, ?, ?)
        """, generate_engines_data())

        # Вставка данных в таблицу ships
        cursor.executemany("""
            INSERT INTO ships (ship, weapon, hull, engine)
            VALUES (?, ?, ?, ?)
        """, generate_ships_data())

        # Сохранение изменений
        conn.commit()
        print("База данных успешно заполнена.")

    except sqlite3.Error as e:
        # logging.info("Database populated successfully.")
        # print(f"Произошла ошибка: {e}")
        conn.rollback()

    finally:
        conn.close()


# if __name__ == "__main__":
#     fill_db()

from db.conn_db import conn_db
from config import TEMP_DB_NAME

def test_123(changed_db):
    with conn_db() as conn:
        cursor = conn.cursor()
        ships_orig = cursor.execute("SELECT * FROM ships").fetchall()

    with conn_db(TEMP_DB_NAME) as conn:
        cursor = conn.cursor()
        ships_new = cursor.execute("SELECT * FROM ships").fetchall()

    # print(ships_orig)
    # print(ships_new)

    for i in range(20):
        for j in range(3):
            # print(i, j)
            if ships_orig[i][j] != ships_new[i][j]:
                print(ships_orig[i][j], ships_new[i][j])


 # ('Ship-200', 'Weapon-8', 'Hull-1', 'Engine-2')]

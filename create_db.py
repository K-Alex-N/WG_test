import sqlite3

connect = sqlite3.connect("WoW.db")
cursor = connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS engines (
     engine text,
     power integer
     )
""")

# data_engines = [
#     ("sdfsdfsdfsdf", 123),
#     ("sdsfdfsdfsdfsdfsdf", 13323)
# ]

data_engines = [
    # ("sdfsdfsdfsdf", 123),
    ("ssdfsdfdfsdfsdfsdf", 13323),
    ("another value", 456)
]

sql_engines = "INSERT INTO engines VALUES (?, ?)"
# sql_engines = "INSERT INTO engines (engine, power)  VALUES (?,?)"
cursor.execute(sql_engines, data_engines)
# """, ("sdfsdfsdfsdf", 123))


connect.commit()

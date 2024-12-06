import sqlite3

connection = sqlite3.connect(":memory")

cursor = connection.cursor()
cursor.execute("CREATE TABLE entry (name TEXT, species TEXT, tank_number INTEGER)")
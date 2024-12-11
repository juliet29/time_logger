from pathlib import Path
import sqlite3


def init_db(connection: sqlite3.Connection):
    DB_INIT_PATH = Path.cwd().parent / "db_creators"
    with open(DB_INIT_PATH / "create.sql", "r") as file:
        create_script = file.read()
    with open(DB_INIT_PATH / "init.sql", "r") as file:
        init_script = file.read()

    with connection:
        connection.executescript(create_script)
        connection.executescript(init_script)

    return connection


def init_in_memory_db():
    connection = sqlite3.connect(":memory:")
    return init_db(connection)


def connect_to_real_db(name):
    connection = sqlite3.connect(name)
    assert connection
    return connection


def check_db(connection: sqlite3.Connection):
    with connection:
        c = connection.cursor()
        c.execute("""SELECT name FROM sqlite_master""")
        res = c.fetchall()
        assert res, "Invalid database connection - No items here :("

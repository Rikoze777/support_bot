import sqlite3


conn = sqlite3.connect('support.db')
# defining a cursor
cursor = conn.cursor()

# creating the table (schema)
cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    user_id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    number 	        INTEGER NOT NULL,
    subscribe_lvl   INTEGER NOT NULL,
    FOREIGN KEY(subscribe_lvl) REFERENCES subscribe(subscribe_id)
    );
CREATE TABLE IF NOT EXISTS subscribe(
    subscribe_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    level        INTEGER NOT NULL,
    created_at   DATE,
    end_at       DATE
    );
CREATE TABLE IF NOT EXISTS status(
    status_id    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    status       VARCHAR(30) NOT NULL
    );
CREATE TABLE IF NOT EXISTS answer(
    subscribe_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    answer       VARCHAR(500) NOT NULL
    );
CREATE TABLE IF NOT EXISTS task(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    text    VARCHAR(500) NOT NULL,
    status 	VARCHAR(30) NOT NULL,
    answer  VARCHAR(500),
    FOREIGN KEY(status) REFERENCES status(status_id),
    FOREIGN KEY(answer) REFERENCES answer(answer_id)
    );
""")
print("\n Tables added.")
# disconnecting ...
conn.close()

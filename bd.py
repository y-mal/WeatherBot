import sqlite3

connection = sqlite3.connect("./sm_app.sqlite", check_same_thread=False)
cursor = connection.cursor()



def create_table_if_not_exists():
    create_table = """
    CREATE TABLE IF NOT EXISTS profilesio (
        id INTEGER PRIMARY KEY,
        personal_id INTEGER NOT NULL,
        name VARCHAR(200) NOT NULL,
        username VARCHAR(200) NULL,
        language VARCHAR(50) NOT NULL,
        favourite_city VARCHAR(100) NULL
    );
    """
    cursor.execute(create_table)
    connection.commit()

add_user = """
INSERT INTO 
  profilesio (personal_id, name, username, language)
VALUES
  (?, ?, ?, ?)
"""

select_all_personal_id_users = """
SELECT personal_id, favourite_city FROM profilesio;"""

check_city = """
SELECT EXISTS(SELECT city FROM profilesio"""

create_table = """
CREATE TABLE profilesio
(id INTEGER PRIMARY KEY,
personal_id INTEGER NOT NULL,
name VARCHAR(200) NOT NULL,
username VARCHAR(200) NULL,
language VARCHAR(50) NOT NULL,
favourite_city VARCHAR(100) NULL)
;"""

update_city = """
UPDATE profilesio
SET favourite_city=?
WHERE personal_id=?;"""



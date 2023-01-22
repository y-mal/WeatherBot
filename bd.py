import sqlite3

connection = sqlite3.connect("/home/yuriy/PycharmProjects/"
                               "NewTelegramBot/sm_app.sqlite", check_same_thread=False)
cursor = connection.cursor()


add_user = """
INSERT INTO 
  profilesio (personal_id, name, username, language)
VALUES
  (?, ?, ?, ?)
"""

select_all_users = """
SELECT personal_id FROM profilesio;"""


create_table = """
CREATE TABLE profilesio
(id INTEGER PRIMARY KEY,
personal_id INTEGER NOT NULL,
name VARCHAR(200) NOT NULL,
username VARCHAR(200) NULL,
language VARCHAR(50) NOT NULL)
;"""

info = (
        1,
        'fds',
        'fssdf',
        'ru',
    )
# cursor.execute(create_table)
# cursor.execute(add_user, [13312312, 'Bobu', 'Rok', 'ru'])
# # connection.commit()
# cursor.execute("SELECT EXISTS(SELECT personal_id from profilesio WHERE personal_id=13312312)")
# if cursor.fetchone()[0] == 0:
#     print('DOes not exist')
# else:
#     cursor.execute(add_user, [1231131232, 'fsdkldslf', 'fjslfsd', 'eng'])
#     connection.commit()

# infof = cursor.execute(select_all_users)
# for i in infof:
#     print(i[0])


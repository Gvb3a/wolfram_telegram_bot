import sqlite3
from colorama import init, Fore, Style
init()


def sql_create():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS frame (
    message TEXT,
    username TEXT,
    time TEXT,
    id INT,
    additionally TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS text (
    text TEXT,
    launch_or_not INT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
    name TEXT,
    id INTEGER PRIMARY KEY,
    mode INT
    )
    ''')

    connection.commit()
    connection.close()


def sql_launch(current_time):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    print(f'The bot {Fore.RED}launches{Style.RESET_ALL} at {current_time}')
    cursor.execute(f"INSERT INTO text(text, launch_or_not) VALUES ('The bot :red[launches] at {current_time}', 1)")

    connection.commit()
    connection.close()


def sql_message(message, name, current_time, user_id, add):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()
    if row is not None:
        if not(name in row[0].split(', ')):
            cursor.execute(f"UPDATE user SET name = '{row[0]}, {name}' WHERE id = {user_id}")
            add += '(update name)'
    else:
        cursor.execute(f"INSERT INTO user(name, id, mode) VALUES ('{name}', {user_id}, 1)")
        add += '(new user)'

    if message == '/mode':
        if row[2]:
            cursor.execute(f"UPDATE user SET mode = 0 WHERE id = {user_id}")
        else:
            cursor.execute(f"UPDATE user SET mode = 1 WHERE id = {user_id}")
        message += f'({row[2]})'

    print(f'{Fore.RED}{message}{Style.RESET_ALL} from {Fore.BLUE}{name}({user_id}){Style.RESET_ALL} at {current_time}. {add}')

    cursor.execute(
        f"INSERT INTO frame(message, username, time, id, additionally) VALUES ('{message}', '{name}', '{current_time}', {user_id}, '{add}')")
    cursor.execute(
        f"INSERT INTO text(text, launch_or_not) VALUES (':red[{message}] from :blue[{name}({user_id})] at {current_time}. {add}', 0)")

    connection.commit()
    connection.close()


def sql_mode(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()

    if row is None:
        cursor.execute(f"INSERT INTO user(id, mode) VALUES ({user_id}, 1)")
        connection.commit()

    connection.close()
    return row[2]

import sqlite3  # library for working with the database
# from colorama import init, Fore, Style  # library for colouring text in print
from datetime import datetime  # library for recognising the current time
# init()  # is used to colour text in the cmd


def sql_launch():
    connection = sqlite3.connect('database.db')  # connecting to the database
    cursor = connection.cursor()  # it is necessary to execute queries to the database
    # create tables, if they did not exist before (new file). This table will store information about the message
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message (
        message TEXT,
        username TEXT,
        time TEXT,
        id INT,
        additionally TEXT
        )
        ''')
    # User information (name, ID and mode) is stored here.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
        name TEXT,
        id INTEGER PRIMARY KEY,
        mode INT
        )
        ''')
    # output information about successful startup to the console and save this information to the database
    current_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    print(f'The bot launches at {current_time}')
    # print(f"The bot {Fore.RED}launches{Style.RESET_ALL} at {current_time}")

    connection.commit()  # Save the changes to the database
    connection.close()  # close the database


def sql_message(message, name, user_id, add):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()

    if row is not None and row[0] is not None:
        if not (name in row[0]):
            cursor.execute(f"UPDATE user SET name = '{row[0]}, {name}' WHERE id = {user_id}")
            add += 'Update name'
    else:
        cursor.execute(f"INSERT INTO user(name, id, mode) VALUES ('{name}', {user_id}, 1)")
        add += 'New user'

    if message == '/mode' and len(message) == 5:
        if row[2]:
            cursor.execute(f"UPDATE user SET mode = 0 WHERE id = {user_id}")
        else:
            cursor.execute(f"UPDATE user SET mode = 1 WHERE id = {user_id}")
        message += str(not(row[2]))

    current_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    print(f'{message} from {name} at {current_time}. {add}')
    # print(f'{Fore.RED}{message}{Style.RESET_ALL} from {Fore.BLUE}{name}({user_id}){Style.RESET_ALL} at {current_time}. {add}')
    cursor.execute(
        f"INSERT INTO message(message, username, time, id, additionally) VALUES ('{message}', '{name}', '{current_time}', {user_id}, '{add}')")

    connection.commit()
    connection.close()


def sql_mode(user_name, user_id):  # function for recognizing the current mode
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")
    row = cursor.fetchone()

    if row is None:
        cursor.execute(f"INSERT INTO user(name, id, mode) VALUES ('{user_name}', {user_id}, 1)")
        connection.commit()
        return 1
    else:
        connection.close()
        return row[2]

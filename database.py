import sqlite3
from colorama import init, Fore, Style
init()

def sql_create():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    sql_frame = '''
    CREATE TABLE IF NOT EXISTS frame (
    message TEXT,
    username TEXT,
    time TEXT,
    additionally TEXT
    )
    '''
    cursor.execute(sql_frame)

    sql_text = '''
    CREATE TABLE IF NOT EXISTS text (
    text TEXT,
    launch_or_not INT
    )
    '''
    cursor.execute(sql_text)

    sql_user = '''
    CREATE TABLE IF NOT EXISTS user (
    id INT,
    mode int
    )
    '''
    cursor.execute(sql_user)

    connection.commit()
    connection.close()

def sql_launch(current_time):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    print(f'The bot {Fore.RED}launches{Style.RESET_ALL} at {current_time}')
    cursor.execute(f"INSERT INTO text(text, launch_or_not) VALUES ('The bot :red[launches] at {current_time}', 1)")
    connection.commit()
    connection.close()

def sql_command(command, name, current_time):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    print(f'{Fore.RED}{command}{Style.RESET_ALL} command from {Fore.BLUE}{name}{Style.RESET_ALL} at {current_time}')
    cursor.execute(f"INSERT INTO frame(message, username, time, additionally) VALUES ('{command}', '{name}', '{current_time}', 'command')")
    cursor.execute(f"INSERT INTO text(text, launch_or_not) VALUES (':red[{command}] command from :blue[{name}] at {current_time}', 0)")

    connection.commit()
    connection.close()

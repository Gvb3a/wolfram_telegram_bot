import sqlite3  # library for working with the database
# from colorama import init, Fore, Style  # library for colouring text in print
from datetime import datetime  # library for recognising the current time
# init()  # is used to colour text in the cmd
import matplotlib.pyplot as plt
import numpy as np


def sql_launch():
    connection = sqlite3.connect('wolfram_database.db')  # connecting to the database
    cursor = connection.cursor()
    # create tables, if they did not exist before (new file)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message (
        message TEXT,
        name TEXT,
        time TEXT,    
        id INT,
        additionally TEXT
        )
        ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
        name TEXT,
        username TEXT,
        id INTEGER PRIMARY KEY,
        num_of_request INT,
        first_request TEXT,
        last_request TEXT
        )
        ''')

    connection.commit()  # Save the changes to the database
    connection.close()  # close the database
    print('Launch')


def sql_user(name: str, username: str, user_id: int):
    connection = sqlite3.connect('wolfram_database.db')
    cursor = connection.cursor()


    row = cursor.execute(f"SELECT * FROM user WHERE id = {user_id}").fetchall()
    time = datetime.now().strftime("%d/%m/%Y")

    if row is None or row == []:
        print(row==[])
        cursor.execute(f"INSERT INTO user(name, username, id, num_of_request, first_request, last_request) VALUES ('{name}', '{username}', {user_id}, 0, '{time}', '{time}')")
    else:
        cursor.execute(f'UPDATE user SET num_of_request = num_of_request+1 WHERE id = {user_id}')
        cursor.execute(f'UPDATE user SET last_request = {time} WHERE id = {user_id}')
    
    """
    row = cursor.execute(f"SELECT * FROM user WHERE id = {user_id}").fetchall()
    if name != row[0]:  # [>>>name<<<, username, id, num_of_request, first_request, last_request]
        cursor.execute(f'UPDATE user SET name = {name} WHERE id = {user_id}')

    if username != row[1]:  # [name, >>>username<<<, id, num_of_request, first_request, last_request]
        cursor.execute(f'UPDATE user SET name = {name} WHERE id = {user_id}')
    """
    
    
    connection.commit()
    connection.close()


def sql_message(message: str, name: str, username:str, user_id:int, add:str):
    connection = sqlite3.connect('wolfram_database.db')
    cursor = connection.cursor()

    sql_user(name, username, user_id)

    if message[0] == '/':
        add = 'Command.' 
    time = datetime.now().strftime("%d.%m.%Y %H:%M")

    cursor.execute(f"INSERT INTO message(message, name, time, id, additionally) VALUES ('{message}', '{name}', '{time}', {user_id}, '{add}')")

    connection.commit()
    connection.close()
    print(f'{message}({add}) by {name} at {time}')





def sql_statistic(file_name, admin):
    # TODO: figure it out and retrieve data normally
    connection = sqlite3.connect('wolfram_database.db')
    cursor = connection.cursor()

    time = datetime.now().strftime('%m.%Y')

    recognition = len(cursor.execute(f"SELECT * FROM message WHERE time LIKE '%{time}' AND additionally LIKE '%Recognition%'").fetchall())
    pictures = len(cursor.execute(f"SELECT * FROM message WHERE time LIKE '%{time}' AND additionally LIKE 'Pictures%'").fetchall())
    text = len(cursor.execute(f"SELECT * FROM message WHERE time LIKE '%{time}' AND additionally LIKE 'Text%'").fetchall())
    command = len(cursor.execute(f"SELECT * FROM message WHERE time LIKE '%{time}' AND additionally LIKE 'Command%'").fetchall())


    fig, ax = plt.subplots(figsize=(8, 8))

    wolfram = [pictures, text, 0, 0]
    photo_recognition = [0, 0, recognition, 0]
    command_list = [0, 0, 0, command]

    labels = ['Command', 'Wolfram', 'Photo recognition']
    legend = ['Pictures mode', 'Text mode', 'Recognition', 'Command']
    data = [command_list, wolfram, photo_recognition]

    # I don't know how it works.
    data = np.array(data).T
    positions = np.arange(len(labels)) + 1

    bottom = np.zeros(len(labels))
    for i, values in enumerate(data):
        ax.bar(positions, values, bottom=bottom, label=legend[i])
        bottom += values

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, bottom.max() + 10)

    ax.set_title('Total:' + str(recognition + pictures + text + command))
    ax.legend()
    plt.savefig(f'{file_name}.png')
    plt.clf()

    connection.close()

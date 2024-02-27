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
    name STR,
    id INT,
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


def sql_command(command, name, current_time, id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    print(f'{Fore.RED}{command}{Style.RESET_ALL} command from {Fore.BLUE}{name}{Style.RESET_ALL} at {current_time}')
    cursor.execute(f"INSERT INTO frame(message, username, time, additionally) VALUES ('{command}', '{name}', '{current_time}', 'command')")
    cursor.execute(f"INSERT INTO text(text, launch_or_not) VALUES (':red[{command}] command from :blue[{name}] at {current_time}', 0)")

    connection.commit()
    connection.close()


def sql_message(text, name, mode, current_time, req_or_ans, add):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    print(f'{req_or_ans} {Fore.GREEN}{text}{Style.RESET_ALL} from {Fore.BLUE}{name}{Style.RESET_ALL} with '
          f'{Fore.RED}{mode}{Style.RESET_ALL} at {current_time}. Additionally: {add}')
    cursor.execute(f"INSERT INTO frame(message, username, time, additionally) VALUES ('{req_or_ans} {text}({mode})', '{name}', '{current_time}', '{add}')")
    cursor.execute(f"INSERT INTO text(text, launch_or_not) VALUES ('{req_or_ans} :green[{text}] from :blue[{name}] with "
                   f":red[{mode}] at {current_time}. Additionally: {add}', 0)")

    connection.commit()
    connection.close()

def streamlit_message_input(text, name, mode, time):
    st.write(f'Request :green[{text}] from :blue[{name}] with {mode} at {time}')


def streamlit_message_output(text, name, time):
    st.write(f'A reply to the :green[{text}] was sent to :blue[{name}] at {time}')
    print(f'A reply to the {Fore.GREEN}{text}{Style.RESET_ALL} was sent to '
          f'{Fore.BLUE}{name}{Style.RESET_ALL} at {time}')

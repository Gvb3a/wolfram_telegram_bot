import streamlit as st

from colorama import Fore, Style, init

init()

def streamlit_command(command, name, current_time):
    st.write(f':red[{command}] command from :blue[{name}] at {current_time}')
    print(f'{Fore.RED}{command}{Style.RESET_ALL} command from {Fore.BLUE}{name}{Style.RESET_ALL} at {current_time}')


def streamlit_launch(current_time):
    st.write(f'The bot :red[launches] at {current_time}')
    print(f'The bot {Fore.RED}launches{Style.RESET_ALL} at {current_time}')

def streamlit_message_input(text, name, mode, time):

    st.write(f'Request :green[{text}] from :blue[{name}] with {mode} at {time}')
    print(f'Request {Fore.GREEN}{text}{Style.RESET_ALL} from {Fore.BLUE}{name}{Style.RESET_ALL} with {mode} at {time}')

def streamlit_message_output(text, name, time):
    st.write(f'A reply to the :green[{text}] was sent to :blue[{name}] at {time}')
    print(f'A reply to the {Fore.GREEN}{text}{Style.RESET_ALL} was sent to '
          f'{Fore.BLUE}{name}{Style.RESET_ALL} at {time}')

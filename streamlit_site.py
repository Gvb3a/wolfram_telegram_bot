import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

db_path = 'D:/PycharmProjects/WolframBot/database.db'

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

def main():
    selected = option_menu(
        menu_title=None,
        options=["Message", "User", "Console"],
        icons=["chat-left", "person-circle", "code-slash"],
        default_index=2,
        orientation="horizontal",
    )

    if selected == "Message":
        cursor.execute("SELECT * FROM message")
        rows = cursor.fetchall()
        st.table(rows)

    if selected == "User":
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        st.dataframe(rows)

    if selected == "Console":
        cursor.execute("SELECT * FROM console")
        rows = cursor.fetchall()
        st.dataframe(rows)

    connection.close()

main()

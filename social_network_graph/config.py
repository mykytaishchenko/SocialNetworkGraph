"""Module for receiving data to log into an
Instagram account from a specified file.

File need to be .csv format

Example of  file struct:
username,<your_username>
password,<your_password>
"""

import csv


def get_account(path: str) -> dict:
    """Function for reading a file at a given
    path and returning data as a dictionary.

    :param path: path to file with data needed to login.
    :return: dict with username and password as keys.
    """
    try:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            return {row[0]: row[1] for row in reader}
    except FileNotFoundError:
        print("No login file")


def login(path):
    global __GLOBAL_LOGIN__
    __GLOBAL_LOGIN__ = get_account(path)


__GLOBAL_LOGIN__ = {}

login("account_to_login.csv")

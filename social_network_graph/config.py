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

    with open(path, 'r') as file:
        reader = csv.reader(file)
        return {row[0]: row[1] for row in reader}


__GLOBAL_LOGIN__ = get_account("account_to_login.csv")

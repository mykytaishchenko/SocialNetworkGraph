"""Module for getting data about Instagram users."""

import os
import pickle
from social_network_graph.user import User
from instagrapi import Client, exceptions
from social_network_graph.config import __GLOBAL_LOGIN__


class Loader:
    """A class with a set of static methods for
    working with data from Instagram users.


    Attributes
    ----------
    Loader.path: str
        contain the path to the directory where user data will be saved.
    Loader.logged: bool
        information about client login. True if the client is logged,
        otherwise False.
    Loader.cl: Client
        the client through which requests to instagram will be made.


    Methods
    -------
    Loader.client_login():
        logs in a client.
    Loader.get(): User
        returns user data by username.
    Loader.check(): bool
        returns True if there is actual local data about users, otherwise False.
    Loader.load(): User
        returns local data about user.
    Loader.save():
        save data about user.
    Loader.get_path(): str
        returns path of file with data about user by username.
    """

    path = "social_network_graph/data"
    logged = False
    cl = Client()

    @staticmethod
    def client_login():
        """Logs in a client.
        After login change class logged variable to True.
        """
        Loader.cl.login(__GLOBAL_LOGIN__["username"], __GLOBAL_LOGIN__["password"])
        Loader.logged = True

    @staticmethod
    def get(username):
        """The function of obtaining data about the user by username.
        If there is actual local data about the user, the method returns them,
        otherwise makes request via the Instagram client.

        :param username: Instagram user by username.
        :return: user data by username.
        """
        if Loader.check(username):
            return Loader.load(username)

        if not Loader.logged:
            Loader.client_login()

        try:
            user_info = Loader.cl.user_info_by_username(username)
        except exceptions.UserNotFound:
            print("No such user.")
            return None

        user_followers = Loader.cl.user_followers(user_info.pk)
        user_following = Loader.cl.user_following(user_info.pk)
        user = User(user_info, user_followers, user_following)

        Loader.save(user, Loader.get_path(username))

        return user

    @staticmethod
    def check(username: str) -> bool:
        """The method checks if there is actual local data about users.

        :param username: Instagram user by username.
        :return: True if there is actual local data about users,
                 otherwise False.
        """
        return os.path.exists(Loader.get_path(username))

    @staticmethod
    def load(username: str) -> User:
        """Method for loading local data about user from
        binary file.

        :param username: Instagram user by username.
        :return: returns local data about user.
        """
        with open(Loader.get_path(username), "rb") as file:
            return pickle.load(file)

    @staticmethod
    def save(user: User, path: str) -> None:
        """Method for saving data about user in binary file.

        :param user: user to save.
        :param path: path to file save.
        """
        with open(path, "wb") as file:
            pickle.dump(user, file)

    @staticmethod
    def get_path(username: str) -> str:
        """Method to get path of file with
        data about user by username.

        :param username: Instagram user by username.
        :return: path to file by username.
        """
        return f"{Loader.path}/{username}.dat"

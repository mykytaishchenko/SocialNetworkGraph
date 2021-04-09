import os
import pickle
from .user import User
from instagrapi import Client


__GLOBAL_LOGIN__ = {"username": "social_network_graph", "password": "SocNetGraph2021#"}


cl = Client()
cl.login(__GLOBAL_LOGIN__["username"], __GLOBAL_LOGIN__["password"])


class Loader:
    path = "data"
    test_mode = False

    @staticmethod
    def get(username):
        if Loader.check(username):
            return Loader.load(username)

        user_info = cl.user_info_by_username(username)
        user_followers = cl.user_followers(user_info.pk)
        user_following = cl.user_following(user_info.pk)
        user = User(user_info, user_followers, user_following)

        if Loader.test_mode:
            Loader.save(user, Loader.get_path(username))

        return user

    @staticmethod
    def check(username: str) -> bool:
        return os.path.exists(Loader.get_path(username))

    @staticmethod
    def load(username: str):
        with open(Loader.get_path(username), "rb") as file:
            return pickle.load(file)

    @staticmethod
    def save(obj, path: str) -> None:
        with open(path, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def get_path(username: str) -> str:
        return f"data/{username}.dat"

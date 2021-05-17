"""A module for demonstrating the capabilities of the
library for receiving data from Instagram."""

from instagrapi import Client
from show_account_info import show
from social_network_graph.user import User


LOGIN = "Insert your Instagram username here."
PASSWORD = "Insert your Instagram password here."


if __name__ == "__main__":
    cl = Client()  # Creating new Instagram client (user)
    cl.login(LOGIN, PASSWORD)  # Login in Instagram account

    user_info = cl.user_info_by_username(LOGIN)  # Getting information about user by username
    user_followers = cl.user_followers(cl.user_id_from_username(LOGIN))  # Getting user followers

    print(f"User name: {user_info.full_name}")
    print(f"User username: {user_info.username}")
    print(f"User id: {user_info.pk}")
    print(f"User biography: {user_info.biography}")
    print(f"User followers: {user_info.follower_count}")
    print(f"User following: {user_info.following_count}")
    print(f"The number of the user posts: {user_info.media_count}")
    print(f"User photo: {user_info.profile_pic_url}")
    print(f"20 user followers usernames: "
          f"{', '.join([user_followers[key].username for key in user_followers.keys()][:20])}.")

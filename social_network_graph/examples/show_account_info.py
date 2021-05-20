from social_network_graph.data_loader import Loader
from social_network_graph.soc_graph import SocialGraph


def show(user):
    print(f"User id: {user.info.pk}")
    print(f"User name: {user.info.full_name}")
    print(f"User username: {user.info.username}")
    print(f"User followers: {user.info.follower_count}")
    print(f"User following: {user.info.following_count}")
    print(f"User biography: {user.info.biography}")
    print(f"The number of the user posts: {user.info.media_count}")
    print(f"User photo: {user.info.profile_pic_url}")
    print(f"20 user followers usernames: "
          f"{', '.join([user.followers[key].username for key in user.followers.keys()][:20])}.")


if __name__ == "__main__":
    Loader.path = "../data"

    user_to_show = Loader.get(input("Enter account username: "))
    show(user_to_show)

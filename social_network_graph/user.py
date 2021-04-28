class User:
    """Class for storing basic information about
    Instagram users.

    Attributes
    ----------
    info: UserMixin
        all basic user information (username, name, country,
        number of subscribers etc).
    followers: dict
        basic information about user followers.
    following: dict
        basic information about user following.
    """
    def __init__(self, info, followers: dict, following: dict):
        """Setting the class attributes specified in the class
        description."""

        self.info = info
        self.followers = followers
        self.following = following

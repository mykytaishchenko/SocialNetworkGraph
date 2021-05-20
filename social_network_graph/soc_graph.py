"""Module with SocialGraph data struct."""

import requests
import networkx as nx
from PIL import Image
from social_network_graph.data_loader import Loader
import matplotlib.pyplot as plt
from social_network_graph.image_processing import round_image, add_images_on_graph


class SocialGraph:
    """A class for building, storing and displaying a social graph.


    Attributes
    ----------
    username_1: str
        username of Instagram user, from which the graph will be built.
    connection: int
        maximum number of connections coming from users.
    graph: Graph
        the graph itself, in which users are recorded and the connections
        between them.


    Methods
    -------
    build_graph():
        graph building.
    add_node():
        adding node to the graph.
    add_edge():
        adding edge to the graph.
    draw():
        plotting a graph on an image.
    add_indent(): str
        adding indents to usernames.
    show():
        showing graph.
    save():
        saving graph in a file.
    """

    def __init__(self, username_1: str, username_2: str = None, connection: int = 10) -> None:
        """Init method.

        :param username_1: username of Instagram user, from which the
                         graph will be built.
        :param connection: maximum number of connections coming from users.
        """
        self.username_1 = username_1
        self.username_2 = username_2
        self.connection = connection
        self.graph = nx.DiGraph()

    def build_path(self, username_1, username_2):
        if username_1 != username_2:

            self.add_node(username_1)

            for user in Loader.get(username_1).followers_usernames:
                if Loader.check(user) and \
                        (self.add_indent(username_1), self.add_indent(user)) not in self.graph.edges():
                    self.add_node(user)
                    self.add_edge(username_1, user)
                    self.build_path(user, username_2)

            for user in Loader.get(username_1).following_usernames:
                if Loader.check(user) and \
                        (self.add_indent(user), self.add_indent(username_1)) not in self.graph.edges():
                    self.add_node(user)
                    self.add_edge(user, username_1)
                    self.build_path(user, username_2)

    def social_path(self):
        self.build_path(self.username_1, self.username_2)

        path = nx.all_pairs_shortest_path(self.graph)

        try:
            path = dict(path)[self.add_indent(self.username_1)][self.add_indent(self.username_2)]
            self.graph = nx.DiGraph()
            for index, user in enumerate(path):
                self.add_node(self.del_indent(user), size=0.14)
                if index != 0:
                    self.add_lopsided_edge(self.del_indent(path[index - 1]), self.del_indent(user))
            return True
        except KeyError:
            self.graph = nx.DiGraph()
            print("No path!")
            return False

    def build_graph(self, loops: int = 1) -> bool:
        """Building a graph. The method gets information about
        the user and followers and builds a graph.

        Nodes are Instagram users, edges are connections between users.
        """
        loops -= 1

        user = Loader.get(self.username_1)

        if user is None:
            return False

        self.add_node(user.info.username, user.info.profile_pic_url)

        foll_and_foll = list(set(user.followers.keys()).intersection(set(user.following.keys())))
        followers_id = [user_id for user_id in foll_and_foll][:self.connection]

        follow = [Loader.get(user.followers[user_id].username) for user_id in followers_id]

        for user_id in followers_id:
            self.add_node(user.followers[user_id].username,
                          user.followers[user_id].profile_pic_url)
            self.add_edge(user.info.username,
                          user.followers[user_id].username)

        for user_id in followers_id:
            for follower in follow:
                if user_id in follower.followers.keys():
                    self.add_lopsided_edge(user.followers[user_id].username,
                                           follower.info.username)

        if loops > 0:
            self.connection //= 5
            for follower in follow:
                self.build_graph(follower.info.username, loops=loops)

        return True

    def add_node(self, value, img_url: str = None, size: float = 0.1) -> None:
        """Adding node to the graph.

        :param value: node value.
        :param img_url: link to user profile pictures.
        :param size: node size.
        """
        if self.add_indent(value) not in self.graph.nodes.keys():
            if img_url is None:
                img_url = Loader.get(value).info.profile_pic_url
            img = round_image(Image.open(requests.get(img_url, stream=True).raw))
            self.graph.add_node(self.add_indent(value), image=img, size=size)

    def add_edge(self, f_item, s_item) -> None:
        """Adding edge to the graph.

        :param f_item: first node.
        :param s_item: second node.
        """
        self.add_lopsided_edge(f_item, s_item)
        self.add_lopsided_edge(s_item, f_item)

    def add_lopsided_edge(self, f_item, s_item) -> None:
        """Adding lopsided edge to the graph.

        :param f_item: first node.
        :param s_item: second node.
        """
        self.graph.add_edge(self.add_indent(f_item),
                            self.add_indent(s_item))

    def draw(self) -> None:
        """Plotting a graph on an image."""
        G = self.graph

        nodes = G.nodes()
        pos = nx.kamada_kawai_layout(G)
        fig = plt.figure(figsize=(16, 9), dpi=150)

        if self.username_2 is None:
            k = 1
        else:
            k = 2
        nx.draw(G, pos, alpha=0.9, nodelist=nodes, node_color='#D98032', node_size=4700*k,
                with_labels=True, font_size=24*k/2, width=1*k, edge_color='#F29C50', font_color='w')

        fig.set_facecolor('#2A3A40')

        ax = plt.gca()
        ax.set_xlim([1.3 * x for x in ax.get_xlim()])
        ax.set_ylim([1.3 * y for y in ax.get_ylim()])

        add_images_on_graph(G, pos, ax)

    @staticmethod
    def add_indent(text: str) -> str:
        """Adding indents to usernames for their correct
        display on the final image.

        :param text: the text to which you want to add indentation.
        :return: indented text.
        """
        return "\n" * 7 + text

    @staticmethod
    def del_indent(text: str) -> str:
        """Delete indents from usernames

        :param text: the text in which you want to del indentation.
        :return: text.
        """
        return text[7:]

    @staticmethod
    def show() -> None:
        """Showing graph."""
        plt.show()

    @staticmethod
    def save(img_name: str, img_format: str = "PNG") -> None:
        """Saving graph as a image.

        :param img_name: name of output image with graph.
        :param img_format: format of output image.
        """
        plt.savefig(f"social_network_graph/{img_name}", format=img_format)

"""Module with SocialGraph data struct."""

import requests
import networkx as nx
from PIL import Image
from .data_loader import Loader
import matplotlib.pyplot as plt
from .image_processing import round_image, add_images_on_graph


class SocialGraph:
    """A class for building, storing and displaying a social graph.


    Attributes
    ----------
    username: str
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
    def __init__(self, username: str, connection: int = 10) -> None:
        """Init method.

        :param username: username of Instagram user, from which the
                         graph will be built.
        :param connection: maximum number of connections coming from users.
        """
        self.username = username
        self.connection = connection
        self.graph = nx.Graph()
        self.build_graph()

    def build_graph(self) -> None:
        """Building a graph. The method gets information about
        the user and followers and builds a graph.

        Nodes are Instagram users, edges are connections between users.
        """
        user = Loader.get(self.username)

        self.add_node(user.info.username, user.info.profile_pic_url)

        counter = 0
        for user_id in user.followers.keys():
            self.add_node(user.followers[user_id].username,
                          user.followers[user_id].profile_pic_url)
            self.add_edge(user.info.username,
                          user.followers[user_id].username)
            if counter > self.connection:
                break
            counter += 1

    def add_node(self, value, img_url, size: float = 0.1) -> None:
        """Adding node to the graph.

        :param value: node value.
        :param img_url: link to user profile pictures.
        :param size: node size.
        """
        img = round_image(Image.open(requests.get(img_url, stream=True).raw))
        self.graph.add_node(self.add_indent(value), image=img, size=size)

    def add_edge(self, f_item, s_item) -> None:
        """Adding node to the graph.

        :param f_item: first node.
        :param s_item: second node.
        """
        self.graph.add_edge(self.add_indent(f_item),
                            self.add_indent(s_item))
        self.graph.add_edge(self.add_indent(s_item),
                            self.add_indent(f_item))

    def draw(self) -> None:
        """Plotting a graph on an image."""
        G = self.graph

        nodes = G.nodes()
        pos = nx.kamada_kawai_layout(G)
        fig = plt.figure(figsize=(16, 9), dpi=100)

        nx.draw(G, pos, alpha=0.9, nodelist=nodes, node_color='#D98032', node_size=4700,
                with_labels=True, font_size=12, width=1, edge_color='#F29C50', font_color='w')

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
    def show() -> None:
        """Showing graph."""
        plt.show()

    @staticmethod
    def save(img_name: str, img_format: str = "PNG") -> None:
        """Saving graph as a image.

        :param img_name: name of output image with graph.
        :param img_format: format of output image.
        """
        plt.savefig(img_name, format=img_format)

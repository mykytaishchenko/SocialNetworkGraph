import requests
import networkx as nx
from PIL import Image
from .data_loader import Loader
import matplotlib.pyplot as plt
from .image_processing import round_image, add_images_on_graph


class SocialGraph:
    def __init__(self, username: str, connection: int = 10):
        self.username = username
        self.connection = connection
        self.graph = nx.Graph()
        self.build_graph()

    def build_graph(self):
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

    def add_node(self, value, img_url, size: float = 0.1):
        img = round_image(Image.open(requests.get(img_url, stream=True).raw))
        self.graph.add_node(self.add_indent(value), image=img, size=size)

    def add_edge(self, f_item, s_item):
        self.graph.add_edge(self.add_indent(f_item),
                            self.add_indent(s_item))
        self.graph.add_edge(self.add_indent(s_item),
                            self.add_indent(f_item))

    def draw(self, with_image: bool = True):
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

        if with_image:
            add_images_on_graph(G, pos, ax)

    @staticmethod
    def add_indent(text: str):
        return "\n" * 7 + text

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save(img_name: str, img_format: str = "PNG"):
        plt.savefig(img_name, format=img_format)

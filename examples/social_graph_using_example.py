"""Module with example of using "Social Graph" struct by creating
and showing graph of the first 10 followers of "social_network_graph"
Instagram account."""

from social_network_graph.data_loader import Loader
from social_network_graph.soc_graph import SocialGraph

if __name__ == "__main__":
    soc_graph = SocialGraph("social_network_graph")
    Loader.test_mode = True  # To disable saving data
    soc_graph.draw()
    soc_graph.show()

from hash import Hash
from soc_graph import SocialGraph

if __name__ == "__main__":
    soc_graph = SocialGraph("social_network_graph")
    Hash.test_mode = True
    soc_graph.draw()
    soc_graph.show()

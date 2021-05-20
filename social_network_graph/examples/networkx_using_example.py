"""Module with example of using "networkx" module by creating
and showing simple graph."""

import networkx as nx
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Creating new graph
    graph = nx.Graph()

    # Setting output image dpi and aspect ratio
    fig = plt.figure(figsize=(16, 9), dpi=50)

    # Adding nodes to the graph
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_node("D")
    graph.add_node("F")

    # Adding edges to the graph
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("D", "A")
    graph.add_edge("B", "D")
    graph.add_edge("A", "C")

    graph.add_edge("A", "F")
    graph.add_edge("B", "F")
    graph.add_edge("C", "F")
    graph.add_edge("D", "F")

    # Drawing graph
    nx.draw(graph, node_color='#D98032', node_size=2000, with_labels=True,
            font_size=12, width=1, edge_color='#F29C50', font_color='w')

    # Fill background
    fig.set_facecolor('#2A3A40')

    # Showing result
    plt.show()

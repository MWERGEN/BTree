import igraph as ig
import matplotlib.pyplot as plt

# Create an iGraph graph
graph = ig.Graph.Famous("petersen")

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Plot the iGraph graph within the Matplotlib axis
layout = graph.layout("kk")
ig.plot(graph, target=ax, layout=layout, bbox=(0, 0, 1, 1), margin=20)

# Retrieve the positions of the nodes within the Matplotlib plot
positions = ax.collections[0].get_offsets()

# Iterate over each node and its position
for i, pos in enumerate(positions):
    x, y = pos

    # Retrieve the label of the current node
    label = graph.vs[i]["name"]

    # Adjust the position and size of the label to fit within the node
    ax.text(x, y, label, ha="center", va="center", fontsize=8, color="white")

# Set the aspect ratio and remove the axes
ax.set_aspect("equal")
ax.axis("off")

# Show the plot
plt.show()
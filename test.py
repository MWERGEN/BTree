import igraph as ig
import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = ig.Graph.Ring(10, directed=True)

layout = g.layout('auto')

def _update_graph(frame):
    # Remove plot elements from the previous frame
    ax.clear()

    # Fix limits (unless you want a zoom-out effect)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    if frame < 1000:
        # Plot subgraph
        gd = g.subgraph(range(frame))
    elif frame == 1000:
        # In the second-to-last frame, plot all vertices but skip the last
        # edge, which will only be shown in the last frame
        gd = g.copy()
        gd.delete_edges(9)
    else:
        # Last frame
        gd = g

    ig.plot(gd, target=ax, layout=layout[:frame], vertex_color="yellow")

    # Capture handles for blitting
    if frame == 0:
        nhandles = 0
    elif frame == 1:
        nhandles = 1
    elif frame < 11:
        # vertex, 2 for each edge
        nhandles = 3 * frame
    else:
        # The final edge closing the circle
        nhandles = 3 * (frame - 1) + 2

    handles = ax.get_children()[:nhandles]
    return handles

fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, _update_graph, 12, interval=500, blit=True)
#plt.ion()
plt.show()
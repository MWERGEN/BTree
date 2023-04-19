import numpy as np
from scipy.spatial import Delaunay
import igraph as ig
import matplotlib.pyplot as plt

np.random.seed(2)
x, y = (2, 3)
g = ig.Graph(17)
g2 = ig.Graph(23, directed=True)

ctr = 0
xVal = 0.9
yVal = 3
x1 = []
y1 = []

x2 = []
y2 = []

while ctr < 15:
    if ctr % 5 == 0:
        xVal += 0.1
        x2.append(xVal - 0.06)
        y2.append(yVal)

    x2.append(xVal + 0.06)
    y2.append(yVal)

    x1.append(xVal)
    y1.append(yVal)
    xVal += 0.12
    ctr += 1

x1.append(1.88)
y1.append(3.5)

x1.append(2.0)
y1.append(3.5)

x2.append(1.82)
y2.append(3.5)

x2.append(1.94)
y2.append(3.5)

x2.append(2.06)
y2.append(3.5)

g.vs['x'] = x1
g.vs['y'] = y1

g2.vs['x'] = x2
g2.vs['y'] = y2

g.vs['label'] = ['1','2','3','4','9','11','17','20','21','69','71','72','74','80','81','10','70']

g2.add_edges([
            (18,3),(19,8),(20,14)
        ])

layout = g.layout('auto')
layout2 = g2.layout('auto')


#delaunay = Delaunay(layout.coords)

#for tri in delaunay.simplices:
#    g.add_edges([
#        (tri[0], tri[1]),
#        (tri[1], tri[2]),
#        (tri[0], tri[2]),
#    ])

g.simplify()
g2.simplify()

fig, ax = plt.subplots()

visual_style = {}
visual_style['vertex_shape'] = 'rectangle'

ig.plot(
    g,
    layout=layout,
    target=ax,
    vertex_size=0.06,
    vertex_color="lightblue",
    edge_width=0.8,
    **visual_style
)

ig.plot(
    g2,
    layout=layout2,
    target=ax,
    vertex_size=0.06,
    vertex_color="lightgray",
    edge_width=0.8,
    **visual_style
)

plt.show()
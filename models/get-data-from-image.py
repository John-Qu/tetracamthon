from skimage import io, color, segmentation
from skimage.future import graph
import networkx as nx
import numpy as np
from scipy import ndimage as ndi
from matplotlib import pyplot as plt
# url = ('http://www.eecs.berkeley.edu/Research/Projects/CS/vision/' 'bsds/BSDS300/html/images/plain/normal/color/108073.jpg')
# ![](https://tva1.sinaimg.cn/large/006y8mN6ly1g6m5vvg74dj32iq0sr43x.jpg)
#[url=][/url]'https://tva1.sinaimg.cn/large/006y8mN6ly1g6m3cswhddj31zb0u0wpq.jpg') # acc curves of jaw and york
url = ('https://tva1.sinaimg.cn/large/006y8mN6ly1g6m5vvg74dj32iq0sr43x.jpg')  \
    # acc curve of jaw
tiger = io.imread(url)
seg = segmentation.slic(tiger, n_segments=30, compactness=40.0, enforce_connectivity=True, sigma=3)
# io.imshow(color.label2rgb(seg, tiger));

# g = graph.rag_mean_color(tiger, seg)
# graph.show_rag(seg, g, tiger);

def add_edge_filter(values, graph):
    center = values[len(values) // 2]
    for neighbor in values:
        if neighbor != center and not graph.has_edge(center, neighbor):
            graph.add_edge(center, neighbor)
    # float return value is unused but needed by `generic_filter`
    return 0.0

def build_rag(labels, image):
    g = nx.Graph()
    footprint = ndi.generate_binary_structure(labels.ndim, connectivity=1)
    _ = ndi.generic_filter(labels, add_edge_filter, footprint=footprint,
                           mode='nearest', extra_arguments=(g,))
    for n in g:
        g.node[n]['total color'] = np.zeros(3, np.double)
        g.node[n]['pixel count'] = 0
    for index in np.ndindex(labels.shape):
        n = labels[index]
        g.node[n]['total color'] += image[index]
        g.node[n]['pixel count'] += 1
    return g


g = build_rag(seg, tiger)
for n in g:
    node = g.node[n]
    node['mean'] = node['total color'] / node['pixel count']
for u, v in g.edges():
    d = g.node[u]['mean'] - g.node[v]['mean']
    g[u][v]['weight'] = np.linalg.norm(d)


def threshold_graph(g, t):
    to_remove = [(u, v) for (u, v, d) in g.edges(data=True)
                 if d['weight'] > t]
    g.remove_edges_from(to_remove)


threshold_graph(g, 10)

map_array = np.zeros(np.max(seg) + 1, int)
for i, segment in enumerate(nx.connected_components(g)):
    for initial in segment:
        map_array[int(initial)] = i
segmented = map_array[seg]
plt.imshow(color.label2rgb(segmented, tiger));

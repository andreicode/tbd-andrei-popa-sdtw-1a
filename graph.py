import os
import json
import networkx as nx
import matplotlib.pyplot as plt

nodes = {}
references = []
matrix = []

def read_dir_get_nodes(directory):
  for x in os.walk(directory):
    dir_path = x[0]
    if dir_path != directory:
      current_node = (dir_path.lstrip('./data/')).strip('\n\r ')
      if os.path.exists(dir_path + '/page.data'):
        nodes[dir_path.lstrip('./data/')] = True
      if os.path.exists(dir_path + '/page.reference'):
        current_node_ref = {}
        current_node_ref['node'] = current_node
        current_node_ref['refs'] = []
        with open(dir_path + '/page.reference') as f:
          for line in f:
            line = line.strip('\n\r ')
            if line:
              current_node_ref['refs'].append(line)
        references.append(current_node_ref)
      read_dir_get_nodes(x[0])

def make_graph():
  for node in references:
    for ref in node['refs']:
      if ref:
        matrix.append([ref, node['node']])


def print_graph():
  G=nx.Graph()
  for key in nodes:
    G.add_node(key)
  for edge in matrix:
    G.add_edge(edge[0], edge[1])
  nx.draw(G, with_labels=True, font_size=6)
  plt.savefig("./res.png")
  plt.show()

def dump_graph():
  with open('result.json', 'w+') as f:
    json.dump(matrix, f)

read_dir_get_nodes('./data')
make_graph()
print_graph()




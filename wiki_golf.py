from bs4 import BeautifulSoup
import requests
import argparse
import json
# import wikipedia

#########################################################################################################

class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance

def dijsktra(graph, initial):
  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes: 
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distance[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited, path

#########################################################################################################
'''
def get_url(word):
	info = wikipedia.page(word)
	url = info.url
	return url
'''
def get_pages():
	'''
	Parses command line arguments to get page titles
	'''
	parser = argparse.ArgumentParser(description='Wikipedia golf')
	parser.add_argument('strings', metavar='page1', type=str, nargs=2,
                   help='Title of pages')
	return parser.parse_args().strings

def get_links(page):
  '''
  Retrieves distinct links in a Wikipedia page.
  '''
  r = requests.get(page)
  soup = BeautifulSoup(r.content, 'html.parser')
  base_url = page[:page.find('/wiki/')]
  links = list({base_url + a['href'] for a in soup.select('p a[href]') if a['href'].startswith('/wiki/')})
  return links






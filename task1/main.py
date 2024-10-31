import json

with open('Graph.json', 'r') as file:
    raw_g = json.load(file)

graph = raw_g['nodes']

for i in graph.keys():
    print(f"{i}: {graph[i]}")

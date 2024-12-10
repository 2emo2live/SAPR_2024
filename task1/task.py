import json


def main(filename):
    with open(filename, 'r') as file:
        raw_g = json.load(file)

    graph = raw_g['nodes']

    for i in graph.keys():
        print(f"{i}: {graph[i]}")


main('Graph.json')

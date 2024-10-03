import json
import csv
import io
from math import log2


class Graph:
    def __init__(self, json_str: str):
        self.down = json.loads(json_str)['nodes']
        self.up = {}
        for i in self.down.keys():
            self.up[i] = []
        for i in self.down.keys():
            for j in self.down[i]:
                self.up[j] = i

    def process(self):
        l = []
        stack_4 = []
        stack_3 = []
        for i in range(len(self.down.keys())):
            l.append([])
            for j in range(5):
                l[i].append(0)
        for i in self.down.keys():
            l[int(i) - 1][0] = len(self.down[i])
            for j in self.down[i]:
                l[int(j) - 1][1] = 1
                l[int(j) - 1][4] += len(self.down[i]) - 1
        for i in self.down.keys():
            if l[int(i) - 1][1] == 0:
                stack_4.append(i)
        while len(stack_4) != 0:
            idx = stack_4.pop()
            for i in self.down[idx]:
                stack_4.append(i)
                l[int(i) - 1][3] = l[int(idx) - 1][1] + l[int(idx) - 1][3]
            if l[int(idx) - 1][0] == 0:
                stack_3.append(idx)
        checked = dict.fromkeys(self.down.keys(), 0)
        while len(stack_3) != 0:
            idx = stack_3.pop(0)
            repeat = 0
            if checked[idx] != 0:
                continue
            ch = True
            for j in self.down[idx]:
                if checked[j] == 0:
                    ch = False
                    continue
            if not ch:
                continue
            for i in self.up[idx]:
                stack_3.append(i)
                l[int(i) - 1][2] += l[int(idx) - 1][0] + l[int(idx) - 1][2]
            checked[idx] = 1
        return l


def calculate_entropy(data: str):
    csv_input = io.StringIO(data)
    reader = csv.reader(csv_input, delimiter=',')
    prep_data = []
    for row in reader:
        prep_data.append(row)

    h = 0
    for row in prep_data:
        for r in row:
            p = int(r) / (len(prep_data) - 1)
            if p != 0:
                h += p * log2(p)
            else:
                h += 0
    return -1 * h


def main(json_str: str):
    graph = Graph(json_str)
    l = graph.process()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(l)
    csv_result = output.getvalue()
    h = calculate_entropy(csv_result)
    return h


with open('Graph.json', 'r') as file:
    raw_g = file.read()
print(main(raw_g))

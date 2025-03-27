from typing import Tuple, Union
import networkx as nx
import numpy as np


def extract_data(
    filepath: str = "problems/assign100.txt", output_type: str = "array"
) -> Tuple[int, Union[np.array,nx.Graph]]:
    with open(filepath, "rt") as f:
        number = int(f.readline().strip().strip("\n"))
        rows = []
        temp = []
        for line in f.readlines():
            temp += [int(x) for x in line.strip().strip("\n").split(" ")]
            if len(temp) >= number:
                rows.append(temp)
                temp = []
        if temp:
            rows += temp
        try:
            assert len(rows) == number
            for row in rows:
                assert len(row) == number
        except AssertionError:
            raise IOError("File contents do not match given pattern.")
        if output_type == "graph":
            g = nx.Graph()
            g.add_nodes_from(range(number), bipartite=0)
            g.add_nodes_from(range(number), bipartite=1)
            for i in range(number):
                for j in range(number):
                    g.add_edge(i, j, weight=rows[i][j])
                return number, g
    return number, np.array(rows)

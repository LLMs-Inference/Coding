import csv
import numpy as np
from collections import defaultdict


def read_and_process_edges(file_path):
    edges = []
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        has_prob = len(headers) >= 3

        for row in reader:
            if len(row) < 2:
                continue  # Skip incomplete rows
            source = row[0].strip()
            target = row[1].strip()

            # Check probability threshold if applicable
            if has_prob and len(row) >= 3:
                try:
                    prob = float(row[2])
                except ValueError:
                    continue  # Skip rows with invalid probability
                if prob < 0.5:
                    continue

            edges.append((source, target))

    # Remove duplicate edges
    edges = list({(s, t) for s, t in edges})

    # Collect all unique nodes
    sources = {s for s, t in edges}
    targets = {t for s, t in edges}
    nodes = sorted(sources.union(targets))

    return edges, nodes


def edge_list_to_adj_list(edge_list, nodes):
    adj_list = {node: [] for node in nodes}
    for s, t in edge_list:
        adj_list[s].append(t)
    return adj_list


def adj_list_to_edge_list(adj_list):
    edge_list = []
    for s in adj_list.keys():  # Traverses the keys of the adjacency list
        edge_list.extend([(s, t) for t in adj_list[s]])
    return edge_list


def edge_list_to_adj_matrix(edge_list, nodes):
    n = len(nodes)
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    adj_matrix = np.zeros((n, n), dtype=int)
    for s, t in edge_list:
        i = node_to_idx[s]
        j = node_to_idx[t]
        adj_matrix[i, j] = 1
    return adj_matrix


def adj_matrix_to_edge_list(adj_matrix, nodes):
    edge_list = []
    n = len(nodes)
    for i in range(n):
        for j in range(n):
            if adj_matrix[i, j] == 1:
                edge_list.append((nodes[i], nodes[j]))
    return edge_list


def adj_list_to_adj_matrix(adj_list, nodes):
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    n = len(nodes)
    adj_matrix = np.zeros((n, n), dtype=int)
    for s in adj_list:
        i = node_to_idx[s]
        for t in adj_list[s]:
            j = node_to_idx[t]
            adj_matrix[i, j] = 1
    return adj_matrix


def adj_matrix_to_adj_list(adj_matrix, nodes):
    adj_list = {node: [] for node in nodes}
    n = len(nodes)
    for i in range(n):
        s = nodes[i]
        for j in range(n):
            if adj_matrix[i, j] == 1:
                adj_list[s].append(nodes[j])
    return adj_list


def test():
    # Test case with probability column
    csv_data_prob = """source,target,prob
A,B,0.6
A,C,0.4
B,C,0.3
C,D,0.7
A,B,0.8
E,F,0.5
F,E,0.5
"""
    with open("test_prob.csv", "w") as f:
        f.write(csv_data_prob)

    edges_prob, nodes_prob = read_and_process_edges("test_prob.csv")
    print({f"{idx}": {node} for idx, node in enumerate(nodes_prob)})
    print(edges_prob)

    expected_edges = {("A", "B"), ("C", "D"), ("E", "F"), ("F", "E")}
    assert set(edges_prob) == expected_edges
    assert nodes_prob == ["A", "B", "C", "D", "E", "F"]

    adj_list_prob = edge_list_to_adj_list(edges_prob, nodes_prob)
    expected_adj_list = {
        "A": ["B"],
        "B": [],
        "C": ["D"],
        "D": [],
        "E": ["F"],
        "F": ["E"],
    }
    assert adj_list_prob == expected_adj_list

    adj_matrix_prob = edge_list_to_adj_matrix(edges_prob, nodes_prob)
    expected_matrix = np.array(
        [
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
        ],
        dtype=int,
    )
    assert np.array_equal(adj_matrix_prob, expected_matrix)

    # Test case without probability column
    csv_data_no_prob = """source,target
A,B
B,C
C,A
A,B
D,E
E,D
"""
    with open("test_no_prob.csv", "w") as f:
        f.write(csv_data_no_prob)

    edges_no_prob, nodes_no_prob = read_and_process_edges("test_no_prob.csv")
    expected_edges_no_prob = {
        ("A", "B"),
        ("B", "C"),
        ("C", "A"),
        ("D", "E"),
        ("E", "D"),
    }
    assert set(edges_no_prob) == expected_edges_no_prob
    assert nodes_no_prob == ["A", "B", "C", "D", "E"]

    print("All tests passed!")


if __name__ == "__main__":
    test()

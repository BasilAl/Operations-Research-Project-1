from typing import Tuple
import numpy as np
from ortools.graph.python import linear_sum_assignment
import os

PROBLEMS_PATH = "problems/"
SOLUTIONS_DIR = "solutions"
if not os.path.exists(SOLUTIONS_DIR):
    os.makedirs(SOLUTIONS_DIR)


def extract_table(
    filepath: str = "problems/assign100.txt",
) -> Tuple[int, np.array]:
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
    return number, np.array(rows)


def lp_solver(filepath: str, verbose: bool = False) -> None:
    count, costs = extract_table(filepath)
    end_nodes_unraveled, start_nodes_unraveled = np.meshgrid(
        np.arange(costs.shape[1]), np.arange(costs.shape[0])
    )
    start_nodes = start_nodes_unraveled.ravel()
    end_nodes = end_nodes_unraveled.ravel()
    arc_costs = costs.ravel()

    assignment = linear_sum_assignment.SimpleLinearSumAssignment()
    assignment.add_arcs_with_cost(start_nodes, end_nodes, arc_costs)
    status = assignment.solve()

    output_path = filepath.replace(".txt", "_solved.txt").replace(
        "problems/", f"{SOLUTIONS_DIR}/"
    )
    with open(output_path, "wt+") as f:
        if status == assignment.OPTIMAL:
            f.write(str(assignment.optimal_cost()) + "\n")
            for i in range(0, assignment.num_nodes()):
                f.write(
                    f"{assignment.right_mate(i)},{i},{assignment.assignment_cost(i)}\n"
                )
        if status == assignment.INFEASIBLE:
            f.write("No assignment is possible.")
        elif status == assignment.POSSIBLE_OVERFLOW:
            f.write("Some input costs are too large and may cause an integer overflow.")
        print("Εγγραφή αποτελεσμάτων στο αρχείο: ", output_path)

    if verbose:
        if status == assignment.OPTIMAL:
            print(f"Total cost = {assignment.optimal_cost()}\n")
            for i in range(0, assignment.num_nodes()):
                print(
                    f"Worker {i} assigned to task {assignment.right_mate(i)}."
                    + f"  Cost = {assignment.assignment_cost(i)}"
                )
        elif status == assignment.INFEASIBLE:
            print("No assignment is possible.")
        elif status == assignment.POSSIBLE_OVERFLOW:
            print("Some input costs are too large and may cause an integer overflow.")


problem_files = os.listdir(PROBLEMS_PATH)
problem_files.sort()

for file_name in problem_files:
    file_path = os.path.join(PROBLEMS_PATH, file_name)

    if os.path.isfile(file_path):
        print(f"Επεξεργασία αρχείου: {file_name}")
        lp_solver(file_path)

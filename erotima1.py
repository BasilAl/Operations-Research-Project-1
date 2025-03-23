from typing import List, Tuple


def extract_table(
    filepath: str = "problems/assign100.txt",
) -> Tuple[int, List[List[int]]]:
    with open(filepath, "rt") as f:
        number = int(f.readline().strip().strip("\n"))
        rows = []
        temp = []
        for line in f.readlines():
            temp += [int(x) for x in line.strip().strip("\n").split(" ")]
            if len(temp) >= 100:
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
    return number, rows


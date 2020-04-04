from collections import defaultdict
import sys

#f = open(r"C:\Users\doa\source\repos\cj2020\cj2020\2-1.txt")
f = sys.stdin


def solve(N, matrix):
    trace = 0
    rows_with_dups = set()
    cols_with_dups = set()
    
    elements_by_row = [set() for x in range(N)]
    elements_by_col = [set() for x in range(N)]
    for r, row in enumerate(matrix):
        for c, x in enumerate(row):
            if r == c :
                trace += x
            s = set()

            if x in elements_by_row[r]:
                rows_with_dups.add(r)
            else:
                elements_by_row[r].add(x)

            if x in elements_by_col[c]:
                cols_with_dups.add(c)
            else:
                elements_by_col[c].add(x)

    str_res = "{0} {1} {2}".format(trace, len(rows_with_dups), len(cols_with_dups))
    return str_res

T = int(f.readline())

for t in range(T):
    N = int(f.readline())
    matrix = []
    for n in range(N):
        matrix += [[int(x) for x in f.readline().split(" ")]]
    print ("Case #{0}: {1}".format(t + 1, solve(N, matrix)))

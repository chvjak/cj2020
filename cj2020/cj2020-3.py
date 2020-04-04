#https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209aa0

from collections import defaultdict
import sys

#f = open(r"C:\Users\doa\source\repos\cj2020\cj2020\2-1.txt")
f = sys.stdin


def solve(N, K):
    # make 

    str_res = ""
    return str_res

T = int(f.readline())

for t in range(T):
    N, K = [int(x) for x in f.readline().split(" ")]
    res, m = solve(N, K)
    print ("Case #{0}: {1}".format(t + 1, res))
    print (m)

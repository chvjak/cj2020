#https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209a9f

from collections import defaultdict
import sys

#f = open(r"C:\Users\doa\source\repos\cj2020\cj2020\4-2.txt")
f = sys.stdin


def solve(digits):
    # make
    str_res = ""
    for prev_d, d in zip([0] + digits, digits + [0]):
        
        if prev_d < d:
            for i in range(prev_d, d):
                str_res += "("
        else:
            for i in range(d, prev_d):
                str_res += ")"
        str_res += str(d)

    return str_res[:-1]

T = int(f.readline())

for t in range(T):
    digits =[int(x) for x in f.readline().strip()]
    print ("Case #{0}: {1}".format(t + 1, solve(digits)))

  
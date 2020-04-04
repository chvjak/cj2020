from collections import defaultdict
import sys

#f = open(r"C:\Users\doa\source\repos\cj2020\cj2020\1-1.txt")
f = sys.stdin


def solve(N, starts, ends, starts_to_activities, ends_to_activities):
    points = set(list(starts.keys()) + list(ends.keys()))
    points = list(points )
    points.sort()

    active_activities = 0
    activity_person = [0] * N
    availability = [True, True] # 0 - C, 1 - J
    for p in points:
        active_activities += starts[p]
        active_activities -= ends[p]

        if active_activities > 2:
            return "IMPOSSIBLE"

        if ends[p]:
            for a in ends_to_activities[p]:
                availability[activity_person[a]] = True

        if starts[p]:
            availability_ix = 0
            for a in starts_to_activities[p]:
                if not availability[availability_ix]:
                    availability_ix += 1

                activity_person[a] = availability_ix
                availability[availability_ix] = False

    str_res = "".join(["CJ"[x] for x in activity_person])

    return str_res

T = int(f.readline())

for t in range(T):
    N = int(f.readline())
    starts = defaultdict(lambda : 0)
    ends = defaultdict(lambda : 0)
    starts_to_activities = defaultdict(set)
    ends_to_activities = defaultdict(set)
    for n in range(N):
        l = f.readline()
        p1, p2 = [int(x) for x in l.split(" ")]

        starts[p1] += 1
        ends[p2] += 1

        starts_to_activities[p1].add(n)
        ends_to_activities[p2].add(n)

    print ("Case #{0}: {1}".format(t + 1, solve(N, starts, ends, starts_to_activities, ends_to_activities)))

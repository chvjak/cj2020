#https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209a9e

# Interactive DB queries
def neg(cb):
    return "0" if cb == "1" else "1"

class MyJudge:
    def __init__(self, _bits, mutations = None):
        self.bits = list(_bits)
        self.i = 1
        self.response = ""
        self.mutations = mutations

    def read(self, query):
        if len(str(query)) < 3:
            if self.i % 10 == 1:
                if self.mutations is not None:
                    if "m" in self.mutations[self.i] :
                        self.mirror()
                    if "n" in self.mutations[self.i] :
                        self.negate()

                else:
                    self.mirror()
                    self.negate()

            self.response = self.bits[int(query) - 1]
            self.i += 1

        else:
            Log("Expected result: {0}".format("".join(self.bits)))
            self.response = "Y" if query == "".join(self.bits) else "N"

    def send(self):
        return self.response

    def mirror(self):
        Log("Mirroring...")
        B = len(self.bits) 
        for i in range(B // 2):
            self.bits[i], self.bits[B - i - 1] = self.bits[B - i - 1], self.bits[i]

    def negate(self):
        Log("Negation...")
        B = len(self.bits) 
        for i in range(B):
            self.bits[i] = neg(self.bits[i])


DEBUG = False
#DEBUG = True

#JUDGE = MyJudge("1111100000")
#JUDGE = MyJudge("11111000001111100001")
#JUDGE = MyJudge("11111101011110110111")
#JUDGE = MyJudge("01110000100111110001")
#JUDGE = MyJudge("00000000000000000000")
JUDGE = MyJudge("10001111011000001110", {1:"", 11:"m", 21:"mn"})

from collections import defaultdict
import sys
f = sys.stdin

ferr = sys.stderr
def Log(msg):
    if DEBUG:
        print(msg, file=ferr)
        ferr.flush()

class JudgeClient:
    def __init__(self):
        self.i = 0

    def send(self, msg):
        self.i += 1
        Log("Sending: {0}".format(msg))

        if DEBUG:
            JUDGE.read(msg)
        else:
            print(msg)
            sys.stdout.flush()
    
        Log("Done sending")

    def read(self):
        Log("Reading response")

        if DEBUG:
            msg = JUDGE.send()
        else:
            msg = f.readline().strip()

        Log("Read response {0}".format(msg))

        return msg 

class MutationDetector:
    def __init__(self, jc, res):
        self.sym_ix = -1
        self.sym_val = -1

        self.asym_ix = -1
        self.asym_val = -1

        self.res = res
        self.jc = jc

    def detect_markers(self, b):
        B = len(self.res)
        if self.res[b - 1] == self.res[B - b]:
            self.sym_ix = b
            self.sym_val = self.res[b - 1]
        else:
            self.asym_ix = b
            self.asym_val = self.res[b - 1]

    def detect_transformations(self, b):
        B = len(self.res)
        if self.jc.i % 10 == 9:
            #dummy read
            self.jc.send(b)
            sink = self.jc.read()

        if self.jc.i % 10 == 0 and b <= B // 2:
            # on request 11, 21, ... analyse sym & asym
            if self.sym_ix != -1:
                self.jc.send(self.sym_ix)
                new_sym_val = self.jc.read()

                if new_sym_val != self.sym_val:
                    Log("Negation detected")
                    self.sym_val = neg(self.sym_val)
                    self.asym_val = neg(self.asym_val)
                    #do negate
                    for j in range(b):
                        self.res[j] = neg(self.res[j])
                        self.res[B - j - 1] = neg(self.res[B - j - 1])

                    ra = "".join([str(x) for x in self.res])
                    re = "".join(JUDGE.bits)
                    Log("Status Eq?: {0},  Exp: {1}, Act: {2}".format(ra == re, re, ra))

            if self.asym_ix != -1:
                self.jc.send(self.asym_ix)
                new_asym_val = self.jc.read()

                if new_asym_val != self.asym_val:
                    Log("Mirroring detected")
                    self.asym_val = neg(self.asym_val)
                    #do mirror, sym might be skipped
                    for j in range(b):
                        self.res[j], self.res[B - j - 1] = self.res[B - j - 1], self.res[j]

                    ra = "".join([str(x) for x in self.res])
                    re = "".join(JUDGE.bits)
                    Log("Status Eq?: {0},  Exp: {1}, Act: {2}".format(ra == re, re, ra))


Log("Started solver")
T, B = [int(x) for x in f.readline().split(" ")]
Log("Read {0}, {1}".format(T, B))

for t in range(T):
    res = [-1] * B

    jc = JudgeClient()
    change_detector = MutationDetector(jc, res)

    b = 1
    sym_ix = -1
    sym_val = -1

    asym_ix = -1
    asym_val = -1

    while b <= B // 2:
        jc.send(b)
        res[b - 1] = jc.read()

        jc.send(B - b + 1)
        res[B - b] = jc.read()

        change_detector.detect_markers(b)
        change_detector.detect_transformations(b)

        b += 1


    jc.send("".join(res))
    response = jc.read()


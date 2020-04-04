#https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209a9e

# Interactive DB queries
def neg(cb):
    return "0" if cb == "1" else "1"

class MyJudge:
    def __init__(self, _bits):
        self.bits = list(_bits)
        self.i = 1
        self.response = ""

    def read(self, query):
        if len(str(query)) < 3:
            if self.i % 10 == 1:
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
JUDGE = MyJudge("01110000100111110001")

from collections import defaultdict
import sys
f = sys.stdin

ferr = sys.stderr
def Log(msg):
    if DEBUG:
        print(msg, file=ferr)
        ferr.flush()

def send(msg):
    Log("Sending: {0}".format(msg))

    if DEBUG:
        JUDGE.read(msg)
    else:
        print(msg)
        sys.stdout.flush()
    
    Log("Done sending")

def read():
    Log("Reading response")

    if DEBUG:
        msg = JUDGE.send()
    else:
        msg = f.readline().strip()

    Log("Read response {0}".format(msg))

    return msg 

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

class ChangeDetector:
    def __init__(self):
        self.sym_ix = -1
        self.sym_val = -1

        self.asym_ix = -1
        self.asym_val = -1

    def detect_markers(self, res, b):
        B = len(res)
        if res[b - 1] == res[B - b]:
            self.sym_ix = b
            self.sym_val = res[b - 1]
        else:
            self.asym_ix = b
            self.asym_val = res[b - 1]

    def detect_transformations(self, jc, res, b):
        B = len(res)
        if jc.i % 10 == 0 and b <= B // 2:
            # on request 11, 21, ... analyse sym & asym
            if self.sym_ix != -1:
                jc.send(self.sym_ix)
                new_sym_val = read()

                if new_sym_val != self.sym_val:
                    Log("Negation detected")
                    self.sym_val = neg(self.sym_val)
                    self.asym_val = neg(self.asym_val)
                    #do negate
                    for j in range(b):
                        res[j] = neg(res[j])
                        res[B - j - 1] = neg(res[B - j - 1])

            if self.asym_ix != -1:
                jc.send(self.asym_ix)
                new_asym_val = read()

                if new_asym_val != self.asym_val:
                    Log("Mirroring detected")
                    self.asym_val = neg(self.asym_val)
                    #do mirror, sym might be skipped
                    for j in range(b):
                        res[j], res[B - j - 1] = res[B - j - 1], res[j]

Log("Started solver")
T, B = [int(x) for x in f.readline().split(" ")]
Log("Read {0}, {1}".format(T, B))

jc = JudgeClient()

for t in range(T):
    res = [-1] * B

    b = 1
    sym_ix = -1
    sym_val = -1

    asym_ix = -1
    asym_val = -1

    i = 0
    while b <= B // 2:
        send(b)
        i += 1
        res[b - 1] = read()

        if i % 10 == 0 and b <= B // 2:
            # on request 11, 21, ... analyse sym & asym
            if sym_ix != -1:
                send(sym_ix)
                i += 1
                new_sym_val = read()

                if new_sym_val != sym_val:
                    Log("Negation detected")
                    sym_val = neg(sym_val)
                    asym_val = neg(asym_val)
                    #do negate
                    for j in range(b):
                        res[j] = neg(res[j])
                        res[B - j - 1] = neg(res[B - j - 1])

            if asym_ix != -1:
                send(asym_ix)
                i += 1
                new_asym_val = read()

                if new_asym_val != asym_val:
                    Log("Mirroring detected")
                    asym_val = neg(asym_val)
                    #do mirror, sym might be skipped
                    for j in range(b):
                        res[j], res[B - j - 1] = res[B - j - 1], res[j]

        send(B - b + 1)
        i += 1
        res[B - b] = read()

        # detect sym & asym
        if res[b - 1] == res[B - b]:
            sym_ix = b
            sym_val = res[b - 1]
        else:
            asym_ix = b
            asym_val = res[b - 1]

        if i % 10 == 0 and b <= B // 2:
            # on request 11, 21, ... analyse sym & asym
            if sym_ix != -1:
                send(sym_ix)
                i += 1
                new_sym_val = read()

                if new_sym_val != sym_val:
                    Log("Negation detected")
                    sym_val = neg(sym_val)
                    asym_val = neg(asym_val)
                    #do negate
                    for j in range(b):
                        res[j] = neg(res[j])
                        res[B - j - 1] = neg(res[B - j - 1])

            if asym_ix != -1:
                send(asym_ix)
                i += 1
                new_asym_val = read()

                if new_asym_val != asym_val:
                    Log("Mirroring detected")
                    asym_val = neg(asym_val)
                    #do mirror
                    for j in range(b):
                        res[j], res[B - j - 1] = res[B - j - 1], res[j]

        b += 1


    send("".join(res))
    response = read()


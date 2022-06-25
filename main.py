from FSA import *
from FSAhelper import *
from Partition import Partition
from debug import *
from isEquivalent import *

def readNFA(id:int):
    """
        Accept input then return a machine

        Format:
            <NFA Name>
            |Q|
            <|Q| lines follow, each with a state name>
            |S|
            <|S| lines follow, each with a stimulus symbol>
            |δ|
            <|δ|, each with a transition of the format <src> <stimulus> <dest>>
            q_I - initial state (guaranteed to only have one)
            |F|
            <|F| lines follow, each with a final state, which is a valid member of Q from above>
    """
    name = input()

    nQ = int(input())
    Q = [input()+str(id) for _ in range(nQ)]

    nS = int(input())
    S = [input() for _ in range(nS)]

    nT = int(input())
    tMap = TransitionMap(S)
    for _ in range(nT):
        src, stimulus, dest = input().split()
        tMap.add_transition(src+str(id), stimulus, dest+str(id))

    qI = input()+str(id)

    nF = int(input())
    F = [input()+str(id) for _ in range(nF)]

    return FSA(name, Q, S, tMap, qI, F)

if __name__ == "__main__":
    M0 = readNFA(0)
    input() # read empty line
    M1 = readNFA(1)

    # check for equivalence
    print("equivalent" if is_equivalent(M0, M1) else "not equivalent")
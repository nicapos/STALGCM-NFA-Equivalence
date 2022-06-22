from FSA import *
from FSAhelper import *
from partition import Partition
from debug import *
from isEquivalent import is_equivalent

def parser():
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
    Q = [input() for _ in range(nQ)]

    nS = int(input())
    S = [input() for _ in range(nS)]

    nT = int(input())
    tMap = TransitionMap(S)
    for _ in range(nT):
        src, stimulus, dest = input().split()
        tMap.add_transition(src, stimulus, dest)

    qI = input()

    nF = int(input())
    F = [input() for _ in range(nF)]

    return FSA(name, Q, S, tMap, qI, F)

def renameFSAstates(fsa:FSA, new_labels:list):
    """
        renames the states of the given FSA based on the given new_labels
        NOTE: # of labels in new_labels should be equal to the # of states.
    """
    if not len(new_labels) == len(fsa.states): # DEBUG
        raise Exception("ERROR: # of labels in new_labels should be equal to the # of states.")

    # 1. Create translation table
    old_labels = list(fsa.states)
    translate = {old_labels[i] : new_labels[i] for i in range(len(old_labels))}

    # 2. Rename states in transition map
    tMap = TransitionMap(fsa.stimulus)

    for src_state, stimulus_dest_pair in fsa.transition.tmap.items():
        new_state = translate[src_state]
        tMap.tmap[new_state] = {}
        for stimulus, pair in stimulus_dest_pair.items():
            tMap.tmap[new_state][stimulus] = translate[pair[0]]
        
    fsa.transition = tMap

    # 3. Rename initial and final states
    fsa.initial_state = translate[fsa.initial_state]
    new_finals = [translate[state] for state in fsa.final_states]
    fsa.final_states = new_finals

    # 4. Rename FSA states
    fsa.states = [translate[state] for state in fsa.states]

if __name__ == "__main__":
    Machines = []
    while True:     # do while
        Machines.append(parser())
        try:
            input()
        except EOFError:
            break

    # 1. print the machines then convert to DFA and reduce
    for M in Machines:
        printFSA(M)
        print()

        convertToDFA(M)
        reduceFSA(M)

        printFSA(M)
        print()

    # 2. rename the machines
    STATE_NAMES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for M in Machines:
        """
            get the first N capital letters in state names
            where N = number of states of the machine (|Q|)
        """
        new_states = [STATE_NAMES.pop(0) for _ in range(len(M.states))]
        renameFSAstates(M, new_states)

    # 3. print the resulting machines
    for M in Machines:
        printFSA(M)
        print()

    # 4. check for equivalence
    print("equivalent" if is_equivalent(Machines[0],Machines[1]) else "not equivalent")
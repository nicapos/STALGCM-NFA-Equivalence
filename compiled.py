class TransitionMap:
    def __init__(self, S:list):
        self.stimulus = S
        self.tmap = {}

    def get_next_state(self, src, stimulus) -> str:
        try:
            return self.tmap[src][stimulus]
        except KeyError:
            return []

    def add_transition(self, src, stimulus, dest):
        if src not in self.tmap.keys():
            self.tmap[src] = {S : [] for S in self.stimulus}

        self.tmap[src][stimulus].append(dest)

class FSA:
    def __init__(self, name:str, Q:list, S:list, delta:TransitionMap, I:str, F:list):
        self.name = name
        self.states = set(Q)
        self.stimulus = set(S)
        self.transition = delta
        self.initial_state = I
        self.final_states = set(F)

    def get_next_state(self, src:str, stimulus:str) -> str:
        return self.transition.get_next_state(src, stimulus)

class Partition:
    def __init__(self, transition_func, stimulus:list, final_states:list, nonfinal_states:list):
        self.set = [list(final_states), nonfinal_states]
        self.stimulus = stimulus
        self.next_state = transition_func # is a method

        self.LIMIT = 10 # DEBUG

    def find_subset(self, state) -> int:
        for i in range( len(self.set) ):
            if state in self.set[i]:
                return i
        return -1

    def step(self):
        if self.LIMIT == 0: # DEBUG
            raise Exception("Partition limit reached.")
        partition_blocks = []

        for subset in self.set:
            block = {}
            for src_state in subset:
                # get subset index of each dest
                indices = ''
                for input in self.stimulus:
                    next_state = ''.join(self.next_state(src_state, input))
                    indices += str(self.find_subset(next_state))

                # if indices not in partition, add it
                if indices not in block.keys():
                    block[indices] = []

                # add src state to partition group with the same indices
                block[indices].append(src_state)

            for new_block in block.values():
                partition_blocks.append(new_block)
        
        self.set = partition_blocks
        self.LIMIT -= 1 # DEBUG

def convertToDFA(fsa:FSA):
    explore_states = [[fsa.initial_state]]   # queue of sets of states to explore
    i = 0   # pointer index for queue

    new_states = []
    new_tMap = TransitionMap(fsa.stimulus)
    new_initial = None
    new_finals = []

    while i < len(explore_states):
        state_list = explore_states[i]      # ex. ['A','B','C']
        state_label = ''.join(state_list)   # ex. 'ABC'

        new_states.append(state_label)      # add states to list of new states
        if any(state == fsa.initial_state for state in state_list):
            new_initial = state_label
        if any(state in fsa.final_states for state in state_list):
            new_finals.append(state_label)

        for input in fsa.stimulus:
            # get next state/s (dest) from current state (src)
            next_states = []
            for S in state_list:
                next_states += fsa.get_next_state(S, input)
            
            next_states = list(set(next_states)) # remove duplicates
            next_states.sort()
            dest = ''.join(next_states)

            # copy transition to new transition map
            new_tMap.add_transition(state_label, input, dest)

            # add next state/s to queue of explore_states if it's not yet there
            if next_states not in explore_states:
                explore_states.append(next_states)

        i += 1

    fsa.states = new_states
    fsa.transition = new_tMap
    fsa.initial_state = new_initial
    fsa.final_states = new_finals

def reduceFSA(fsa:FSA):
     # 1. prepare sets for partition. 1 set for final states, 1 set for non-final states
    final_states = fsa.final_states
    nonfinal_states = [state for state in fsa.states if state not in final_states]
    partition_algo = Partition(fsa.get_next_state, fsa.stimulus, final_states, nonfinal_states)

    # 2. partition until 2 consecutive partitions produce the same output (aka wala nang ipapartition sa prev partition)
    prev_partition_set = None
    while prev_partition_set != partition_algo.set:
        prev_partition_set = partition_algo.set
        partition_algo.step()

    # 3. update FSA based on partition subsets

    new_Q = []
    new_I = None
    new_F = []
    for subset in partition_algo.set:
        repr = fsa.initial_state if fsa.initial_state in subset else subset[0]
        new_Q.append(repr)

        if any(state == fsa.initial_state for state in subset):
            new_I = repr
        if any(state in fsa.final_states for state in fsa.states) and subset != ['']:
            new_F.append(repr)

    fsa.states = set(new_Q)
    fsa.initial_state = new_I
    fsa.final_states = new_F

    # 3.2 update transitions
    new_tMap = TransitionMap(fsa.stimulus)
    for src_state in new_Q:
        for input in fsa.stimulus:
            old_dest = fsa.get_next_state(src_state, input)[0]
            i = partition_algo.find_subset(old_dest)
            new_dest = new_Q[i]
            new_tMap.add_transition(src_state, input, new_dest)

    fsa.transition = new_tMap

def renameFSAstates(fsa:FSA, new_labels:list):
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

def is_equivalent(fsa1:FSA, fsa2:FSA) -> bool:
    # 0. Check if both FSAs have the same stimulus. If not, matic not-equivalent
    if fsa1.stimulus != fsa2.stimulus:
        return False

    # 1. convert to DFA then reduce
    convertToDFA(fsa1)
    reduceFSA(fsa1)
    convertToDFA(fsa2)
    reduceFSA(fsa2)

    # 2. rename the machines (to prevent them from having the same state names)
    STATE_NAMES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    new_states1 = [STATE_NAMES.pop(0) for _ in range(len(fsa1.states))]
    renameFSAstates(fsa1, new_states1)

    new_states2 = [STATE_NAMES.pop(0) for _ in range(len(fsa2.states))]
    renameFSAstates(fsa2, new_states2)

    # 3. Prepare sets for partition. 1 set for final states, 1 set for non-final states
    final_states = list(fsa1.final_states) + list(fsa2.final_states)
    nonfinal_states = [S for S in list(fsa1.states) + list(fsa2.states) if S not in final_states]

    # 4. Prepare joint transition map for the two FSAs
    def get_next_state(src, input):
        if src in fsa1.states:
            return fsa1.get_next_state(src, input)
        elif src in fsa2.states:
            return fsa2.get_next_state(src, input)

    partition_algo = Partition(get_next_state, fsa1.stimulus, final_states, nonfinal_states)

    prev_partition_set = None
    while True:
        if prev_partition_set == partition_algo.set:
            break
        elif partition_algo.find_subset(fsa1.initial_state) != partition_algo.find_subset(fsa2.initial_state):
            break

        prev_partition_set = partition_algo.set
        partition_algo.step()

    return partition_algo.find_subset(fsa1.initial_state) == partition_algo.find_subset(fsa2.initial_state)

def parser():
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

if __name__ == "__main__":
    Machines = []
    while True:     # do while
        Machines.append(parser())
        try:
            input()
        except EOFError:
            break

    # check for equivalence
    print("equivalent" if is_equivalent(Machines[0],Machines[1]) else "not equivalent")
from FSA import *
from partition import Partition
from FSAhelper import *

def is_equivalent(fsa1:FSA, fsa2:FSA) -> bool:
    """
        Checks if the two given FSAs are equivalent. Returns bool (True or False)
        NOTE: Buggy to if you enter the two FSAs without making it a reduced DFA.
              Call convertToDFA() and reduceFSA() before calling this method.
    """
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

    """
        3. Partition until...
            2 consecutive partitions produce the same output (aka wala nang ipapartition sa prev partition)
            (prev_partition_set == partition_algo.set)
            OR
            the two initial states are no longer in the same subset/block
            partition_algo.find_subset(fsa1.initial_state) != partition_algo.find_subset(fsa2.initial_state)

            To get the subset/block number: partition_algo.find_subset(<state>)
    """
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

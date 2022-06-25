from functools import reduce
from src.FSA import *
from Partition import Partition
from FSAhelper import *

def findEquivalents(FSAs:list) -> list:
    """
        Given a list of NFAs (NFAs), return a list of of equivalent machines, grouped by clusters.
        Ex. [ [M0, M1, M3], [M2, M5], [M4] ]
    """
    # 1. Convert each NFA to DFA then reduce.
    for M in FSAs:
        convertToDFA(M)
        reduceFSA(M)

    # 2. Prepare sets for partition. 1 set for final states, 1 set for non-final states
    final_states = []
    for M in FSAs:
        final_states += list(M.final_states) 

    nonfinal_states = []
    for M in FSAs:
        nonfinal_states += [S for S in M.states if S not in final_states]

    # 3. Prepare joint transition map for all FSAs
    def get_next_state(src, input):
        for M in FSAs:
            if src in M.states:
                return M.get_next_state(src, input)

    # 4. Partition until 2 consecutive partitions produce the same output (aka wala nang ipapartition sa prev partition)
    partition_algo = Partition(get_next_state, FSAs[0].stimulus, final_states, nonfinal_states)

    prev_partition_set = None
    while not prev_partition_set == partition_algo.set:
        prev_partition_set = partition_algo.set
        partition_algo.step()

    # 5. Group machines by the partition block number of its initial state. (store its machine name)
    # (If the initial states of two machines are still in the same block, then they are equivalent.)
    result = []
    for block in partition_algo.set:
        cluster = []
        for M in FSAs:
            if M.initial_state in block:
                cluster.append(M.name)

        if cluster != []:
            cluster.sort()
            result.append(cluster)

    return result


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

    # 2. Prepare sets for partition. 1 set for final states, 1 set for non-final states
    final_states = list(fsa1.final_states) + list(fsa2.final_states)
    nonfinal_states = [S for S in list(fsa1.states) + list(fsa2.states) if S not in final_states]

    # 3. Prepare joint transition map for the two FSAs
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

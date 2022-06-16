"""
NOTE: buggy pa to

ISSUE:
    If the two FSAs have states na same name, malilito si joint transition map
    Ex. FSA1 has a state named 'Q0' pero FSA2 also has a state named 'Q0'
        di alam ni get_next_state kung san sya kukuha ng dest state
        by default, sa FSA1 nya muna iccheck

POSSIBLE SOLUTION:
    Create a new method that renames all states in an FSA
    (tho you also have to rename the states in its TransitionMap so baka mahaba haba to)
    tas sa start ng is_equivalent(), call that method to rename the machines from A to Z (or hanggang saan aabot)

    method = function btw
    w3schools has python cheatsheet dun ko ginogoogle lahat HSHAHAHA
"""

from FSA import *
from partition import Partition

def is_equivalent(fsa1:FSA, fsa2:FSA) -> bool:
    """
        Checks if the two given FSAs are equivalent. Returns bool (True or False)
        NOTE: Buggy to if you enter the two FSAs without making it a reduced DFA.
              Call convertToDFA() and reduceFSA() before calling this method.
    """
    # 0. Check if both FSAs have the same stimulus. If not, matic not-equivalent
    if fsa1.stimulus != fsa2.stimulus:
        return False

    # 1. Prepare sets for partition. 1 set for final states, 1 set for non-final states
    final_states = list(fsa1.final_states) + list(fsa2.final_states)
    nonfinal_states = [S for S in list(fsa1.states) + list(fsa2.states) if S not in final_states]

    # 2. Prepare joint transition map for the two FSAs
    def get_next_state(src, input):
        if input in fsa1.states:
            return fsa1.get_next_state(src, input)
        elif input in fsa2.states:
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

        prev_partition_set = partition_algo
        partition_algo.step()

    return partition_algo.find_subset(fsa1.initial_state) == partition_algo.find_subset(fsa2.initial_state)

from FSA import *
from partition import Partition

def convertToDFA(fsa:FSA):
    """
    converts the given FSA into DFA using BFS
    (updates the given FSA, doesn't return anything)
    """
    explore_states = [fsa.initial_state]   # queue of sets of states to explore
    i = 0       # pointer index for queue

    new_states = []
    new_tMap = TransitionMap(fsa.stimulus)

    while i < len(explore_states):
        state_list = explore_states[i]      # ex. ['A','B','C']
        state_label = ''.join(state_list)   # ex. 'ABC'

        new_states.append(state_label)      # add states to list of new states (to update later)

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

def reduceFSA(fsa:FSA):
    """
    reduces the FSA given
    (updates its transition map and states, doesn't return anything)
    NOTE: magbbug dito if di pa sya nacconvert to DFA so convert to DFA muna
    """
    # 1. prepare sets for partition. 1 set for final states, 1 set for non-final states
    final_states = fsa.final_states
    nonfinal_states = [state for state in fsa.states if state not in final_states]
    partition_algo = Partition(fsa, final_states, nonfinal_states)

    # 2. partition until 2 consecutive partitions produce the same output (aka wala nang ipapartition sa prev partition)
    prev_partition_set = None
    while prev_partition_set != partition_algo.set:
        prev_partition_set = partition_algo
        partition_algo.step()

    # 3. update FSA based on partition subsets
    """
        For each subset in partition, let one state be the "representative" for each subset
            If may initial state sa subset, let that be the "representative"
            If walang initial state, let the first state be the "representative"
        Store "representatives" in new_Q list 
        Example:
            partition_algo.set = [ ['A', 'B', 'D'], ['C', 'E'], ['F']  ] ; 'E' is an initial state
            partition_algo.set[0] = ['A', 'B', 'D']     no initial state        sub_rep[0] = 'A'
            partition_algo.set[1] = ['C', 'E']          E is an initial state   sub_rep[1] = 'E'
            partition_algo.set[2] = ['F']               no initial state        sub_rep[2] = 'A'
    """
    new_Q = []
    for subset in partition_algo.set:
        new_Q.append(fsa.initial_state if fsa.initial_state in subset else subset[0])

    fsa.states = set(new_Q) # update states

    # 3.2 update transitions
    new_tMap = TransitionMap(fsa.stimulus)

    for src_state in new_Q:
        for input in fsa.stimulus:
            old_dest = fsa.get_next_state(src_state, input)
            i = partition_algo.find_subset(old_dest)
            new_dest = new_Q[i]
            new_tMap.add_transition(src_state, input, new_dest)

    fsa.transition = new_tMap
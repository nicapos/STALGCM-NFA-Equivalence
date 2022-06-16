from FSA import *

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
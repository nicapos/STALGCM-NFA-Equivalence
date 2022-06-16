class TransitionMap:
    def __init__(self, S:list):
        self.stimulus = S
        self.tmap = {}

    def get_next_state(self, src:str, stimulus:str) -> str:
        return self.tmap[src][stimulus]

    def add_transition(self, src:str, stimulus:str, dest:str):
        if src not in self.tmap.keys():
            self.tmap[src] = {S : [] for S in self.stimulus}

        self.tmap[src][stimulus].append(dest)

class FSA:
    def __init__(self, Q:list, S:list, delta:TransitionMap, I:str, F:list):
        self.states = set(Q)
        self.stimulus = set(S)
        self.transition = delta
        self.initial_state = I
        self.final_states = set(F)

        """
            Checks if this FSA is an NFA.
            This FSA is NFA if...
                it has an empty string transition (TODO)
                or there are multiple state transitions
        """
        for transition in delta.tmap.values():
            if any( not (len(stimulus_list) == 1) for stimulus_list in transition.values() ):
                self.is_NFA = True
                break

    def get_next_state(self, src:str, stimulus:str) -> str:
        return self.transition.get_next_state(src, stimulus)
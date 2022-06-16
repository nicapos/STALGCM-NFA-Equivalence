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
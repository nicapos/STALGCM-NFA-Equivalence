from FSA import FSA

class Partition:
    def __init__(self, transition_func, stimulus:list, final_states:list, nonfinal_states:list):
        self.set = [list(final_states), nonfinal_states]
        self.stimulus = stimulus
        self.next_state = transition_func # is a method

    """
        Finds the subset index of a state.
        Example:
            [ ['A', 'B', 'D'], ['C', 'E'], ['F']  ]
            find_subset('E') returns 1, find_subset('B') returns 0
    """
    def find_subset(self, state) -> int:
        for i in range( len(self.set) ):
            if state in self.set[i]:
                return i
        return -1

    """
        Run the partitioning algorithm for 1 step. Updates set at self.set
        Example:
            self.set is updated to [ ['A', 'B'], ['C', 'D', 'E'], ['F'] ]
    """
    def step(self):
        partition_blocks = []
        """
            dict where key -> indices, value -> states.
            Example: {
                '012': ['A', 'B']
                '100': ['C', 'D', 'E']
                '222': ['F']
            }
        """

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
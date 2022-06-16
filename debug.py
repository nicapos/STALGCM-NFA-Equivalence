from FSA import FSA

"""
Methods needed for debugging.
"""
def print_FSA(fsa:FSA): # for debugging only
    max_name = max(len(q) for q in fsa.states) # longest state name
    max_dests = max(max(len(dest) for dest in dests.values()) for dests in fsa.transition.tmap.values()) # most num of dests for one src (NFAs only)
    cell_length = max_name * max_dests + 3

    def format_cell(cell):
        if cell == '' or cell == [] or cell == ['']:
            return '{}'.ljust(cell_length)
        elif type(cell) is list:
            return (','.join(cell)).ljust(cell_length)
        return cell.ljust(cell_length)

    # print header
    print(fsa.name)
    print(' '*cell_length + ''.join(stimulus.ljust(cell_length) for stimulus in fsa.stimulus))

    for src_state in fsa.states:
        # format state name
        src = src_state
        if src_state in fsa.final_states:
            src += '*'
        if src_state == fsa.initial_state:
            src = '>' + src

        # print row
        print(format_cell(src) + ''.join(format_cell(fsa.get_next_state(src_state, input)) for input in fsa.stimulus))
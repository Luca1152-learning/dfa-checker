import sys

from load import load


def is_accepted_by_dfa(dfa_path, word):
    sigma, start_state, end_states, transitions_dict = load(dfa_path)
    current_state = start_state
    while word:
        current_letter = word[0]
        if (current_state, current_letter) not in transitions_dict:
            return False
        current_state = transitions_dict[(current_state, current_letter)]
        word = word[1:]
    return current_state in end_states


print("accept" if is_accepted_by_dfa(sys.argv[1], sys.argv[2]) else "reject")

def load(path):
    lines = [line.strip() for line in open(path, "r").readlines()
             if not line.startswith("#") and not line.isspace()]
    end_indices = [index for index, line in enumerate(lines) if line == "End"]

    sigma, states, transitions_list = [], [], []
    start_states, end_states = [], []

    start_index = 0
    for i, end_index in enumerate(end_indices):
        if lines[start_index] == "Sigma:":
            sigma.extend(lines[start_index + 1:end_index])
        elif lines[start_index] == "States:":
            states.extend(lines[start_index + 1:end_index])
            for state_index, state in enumerate(states):
                if "S" in state:
                    start_states.append(state_index)
                    states[state_index] = state.split(",")[0]
                if "F" in state:
                    end_states.append(state_index)
                    states[state_index] = state.split(",")[0]
        elif lines[start_index] == "Transitions:":
            transitions_list.extend(lines[start_index + 1:end_index])
        start_index = end_index + 1
    if len(start_states) < 1:
        raise ValueError("No start state given.")
    elif len(start_states) > 1:
        raise ValueError("Too many start states given.")

    # Check transitions
    transitions_dict = {}
    for transition in transitions_list:
        state_a, word, state_b = [text.strip() for text in transition.split(",")]

        if not state_a in states or not state_b in states or not word in sigma:
            raise ValueError(f"The transition '{transition}' is invalid.")

        transitions_dict[state_a, word] = state_b
    return sigma, states[start_states[0]], [states[index] for index in end_states], transitions_dict

class DFA:
    def __init__(self):
        """Initializes the instance with appropriately empty fields"""

        # States
        self._states_count = 0
        self._start_state = None
        self._final_states = []

        # Others
        self._transitions = {}

    def load_from_file(self, path: str) -> str:
        """
        Loads the DFA from the given path into this instance and returns the file's remaining content
        that wasn't parsed.
        """

        # Split the input file into lines
        file_lines = [line.strip() for line in open(path, "r").readlines()]

        # Parse the values from line `0`
        self._states_count, transitions_count = (int(x) for x in file_lines[0].split(' '))

        # Parse the transitions from lines [1, transitions_count]
        for transitionIndex in range(transitions_count):
            transition_line = file_lines[1 + transitionIndex]
            transition_start, transition_end, symbol = transition_line.split(' ')
            self._transitions[int(transition_start), symbol] = int(transition_end)

        # Parse the start state from line `transitions_count + 1`
        self._start_state = int(file_lines[transitions_count + 1])

        # Parse the final states line `(transitions_count + 1) + 1`
        self._final_states = [int(state) for state in file_lines[transitions_count + 2].split(" ")[1:]]

        # Return the rest of the file, if there's anything left
        return "\n".join(file_lines[transitions_count + 3:])

    def is_in_language(self, word):
        """Returns the path used for obtaining the word if it's in the language and [] otherwise."""

        # At first, all words are in the language
        in_language = True

        # The path traversal begins at the start state
        current_state = self._start_state
        path = [current_state]

        # The first symbol in the word is continuously stripped. If the word ends up being "",
        # the algorithm should stop.
        #
        # If, midway, the word was found not to be in the language, the algorithm should also stop.
        while word and in_language:
            # The symbol to be checked for any path leading to it from the current state.
            # It's the first letter because the word is read from left to right.
            current_symbol = word[0]

            # No path leads to the current symbol, so the algorithm stops
            if (current_state, current_symbol) not in self._transitions:
                in_language = False
                break

            # A path to the current symbol was found, so the current_state is updated with the
            # state found, which is also appended to the path
            current_state = self._transitions[(current_state, current_symbol)]
            path.append(current_state)

            # Continue with the next step of the algorithm by stripping the first letter
            word = word[1:]

        # If, by the end of the algorithm, the word is still in the language, we should make sure that
        # the state we arrived at is a final state for it to really be in the language.
        #
        # If the word wasn't in the language and we were to check if the current state is a final one,
        # we could have had a false positive - a word whose path traversal *abruptly* ended at a final
        # state would also be marked as being in the language.
        if in_language:
            in_language = current_state in self._final_states

        # If the word is in the language, return the path.
        # Otherwise, return an empty list -- and not the path regardless, since it would always contain one
        # element, the start state. So if a word is not in the language, the path is not necessarily empty.
        return path if in_language else []

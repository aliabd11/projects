from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> x1 = {"hungry", "hippo"}
        >>> w1 = WordLadderPuzzle("same", "cost", x1)
        >>> x2 = {"hippo", "hungry"}
        >>> w2 = WordLadderPuzzle("same", "cost", x2)
        >>> w1.__eq__(w2)
        True

        >>> x1 = {"meow", "cat"}
        >>> w1 = WordLadderPuzzle("same", "cost", x1)
        >>> x2 = {"woof", "cat"}
        >>> w2 = WordLadderPuzzle("different", "cost", x2)
        >>> w1.__eq__(w2)
        False
        """
        return (type(other) == type(self) and
                self._from_word == other._from_word and self._to_word ==
                other._to_word and self._word_set == other._word_set)

    def __str__(self):
        """
        Return a human-readable string representation of WordLadderPuzzle self.

        >>> x1 = {"hungry", "hippo"}
        >>> w1 = WordLadderPuzzle("beginning", "end", x1)
        >>> print(w1)
        beginning to end
        """
        return "{0} to {1}".format(self._from_word, self._to_word)

    def extensions(self):
        """
        Returns all possible configurations where the new from_word differs by a
        single letter to one of those in self._chars
        from the previous from_word
        @type: self: Puzzle
        @return: list[Puzzle]

        >>> x1 = {"fad", "rad"}
        >>> w1 = WordLadderPuzzle("had", "dad", x1)
        >>> a = w1.extensions()
        >>> b = [WordLadderPuzzle("fad", "dad", x1)\
                ,WordLadderPuzzle("rad", "dad", x1)]
        >>> a == b
        True
        """
        index = 0
        list_of_configs = []
        word = self._from_word
        goal = self._to_word
        while index < len(word) - 1:  # Index to go through each char in word
            list_word = list(word)  # Strings are immutable so needed to use a list
            if word[index] == goal[index]:  # if from word has same letter as the to word, move to next index
                    index += 1
            for char in self._chars:
                if char != word[index]:
                    list_word[index] = char
                    new_word = ''.join(list_word)
                    if new_word in self._word_set:  # Adds all valid permutations of word
                        list_of_configs.append(WordLadderPuzzle(new_word,
                                                self._to_word, self._word_set))
            index += 1
        return list_of_configs  # Returns list[Puzzle] of all valid permutations

    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.
        Solved when from_word is the same as to_word.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> x = {"hungry", "hippo"}
        >>> w = WordLadderPuzzle("same", "same", x)
        >>> w.is_solved()
        True

        >>> x = {"hungry", "hippo"}
        >>> w = WordLadderPuzzle("same", "different", x)
        >>> w.is_solved()
        False
        """
        return self._from_word == self._to_word

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))

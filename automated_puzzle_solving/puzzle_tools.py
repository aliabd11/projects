"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    # Omitted docstring for DFS as not feasible, example would be too long, @Merciful/Benevolent TA
    # Source: Ideas for algorithm from below websites:
    # https://courses.cs.washington.edu/courses/cse326/03su/homework/hw3/dfs.html
    # https://en.wikipedia.org/wiki/Depth-first_search

    visited = set()  # Set discovered to be a better choice than a list

    def _dfs(puzzle, visited):
        visited.add(str(puzzle))  # Str reps are hashable for the set because they're immutable
        if puzzle.is_solved():
            return PuzzleNode(puzzle)
        for p in puzzle.extensions():
            if str(p) not in visited:
                result = _dfs(p, visited)
                if result:
                    return PuzzleNode(p, [result])
    return _dfs(puzzle, visited)


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    """

    # Omitted docstring for BFS as not feasible, example would be too long

    # Source: Ideas for algorithm found from below sites:
    # http://web.stanford.edu/class/archive/cs/cs106b/cs106b.1134/handouts/15-Assignment2.pdf
    # handouts/15-Assignment2.pdf (Provided)
    # https://en.wikipedia.org/wiki/Breadth-first_search

    def _bfs(solution):
        if not solution:
            return
        while solution.parent:
            # if not solution:
            child = solution
            solution = solution.parent
            solution.children = [child]
        return solution

    root = PuzzleNode(puzzle)
    queue = deque()
    visited = set()
    queue.append(root)
    sol = None
    while len(queue) != 0:  # While the queue isn't empty
        current = queue.popleft()
        if str(current) not in visited:
            visited.add(str(current))
            if current.puzzle.is_solved():
                sol = current
                break  # Once solved break out
            if current.puzzle.fail_fast():
                continue
            for p in current.puzzle.extensions():
                node = PuzzleNode(puzzle=p, parent=current)
                queue.append(node)

    return _bfs(sol)


class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
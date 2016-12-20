from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """

        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> m1 = MNPuzzle(start_grid, target_grid)
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid2 = (("*", "2", "3"), ("1", "4", "5"))
        >>> m2 = MNPuzzle(start_grid2, target_grid2)
        >>> m1.__eq__(m2)
        True

        >>> target_grid3 = (("3", "2", "1"), ("5", "4", "*"))
        >>> start_grid3 = (("*", "2", "3"), ("1", "5", "4"))
        >>> m3 = MNPuzzle(start_grid2, target_grid3)
        >>> m1.__eq__(m3)
        False

        """
        return (type(other) == type(self) and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __str__(self):
        """
        Return a human readable string representation of MNPuzzle self.

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> m1 = MNPuzzle(start_grid, target_grid)
        >>> print(m1)
        * 2 3
        1 4 5
        """
        table = ""
        row_count = 0
        for row in self.from_grid:  # Goes through rows, adds to table
            col_count = 0
            for i in row:
                if col_count < len(row)-1:
                    table += (i + " ")
                    col_count += 1
            if row_count < len(self.from_grid)-1:
                table += (i + '\n')
                row_count += 1
            else:
                table += i
        return table  # Returns a table str representing the MNPuzzle

    def extensions(self):
        """
        Return list of extensions of MNPuzzle self. Legal extensions are configurations that can be reached
        by swapping one symbol to the left, right, above, or below "*" with "*"


        @type self: MNPuzzle
        @rtype: List[MNPuzzle]

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> x = MNPuzzle(start_grid, target_grid)
        >>> a = MNPuzzle((("1", "2", "3"), ("*", "4", "5")), target_grid)
        >>> b = MNPuzzle((("2", "*", "3"), ("1", "4", "5")), target_grid)
        >>> print(x.extensions() == [a,b])
        True
        """

        def swap(map, x1, x2, y1, y2):
            '''
            Swaps the position of '*' with the other item at (x2,y2)
            @param map:
            @param x1: int
            @param x2: int
            @param y1: int
            @param y2: int
            @return: tuple[tuple[str]]
            '''
            temp = [j[:] for j in map]
            temp[y1][x1], temp[y2][x2] = temp[y2][x2], temp[y1][x1]
            return tuple(tuple(k) for k in temp)

        # for loops iterate through the coordinates
        # if statement checks if a potential move is within the index/map
        combos = []
        origState = [list(x) for x in self.from_grid]
        for y in range(len(self.from_grid)):
            for x in range(len(self.from_grid[0])):
                if origState[y][x] == '*':
                    if 0 <= y-1 < len(self.from_grid):
                        combos.append(MNPuzzle(swap(origState, x, x, y, y-1),
                                               self.to_grid))
                    if 0 <= y+1 < len(self.from_grid):
                        combos.append(MNPuzzle(swap(origState, x, x, y, y+1),
                                               self.to_grid))
                    if 0 <= x-1 < len(self.from_grid[0]):
                        combos.append(MNPuzzle(swap(origState, x, x-1, y, y),
                                               self.to_grid))
                    if 0 <= x+1 < len(self.from_grid[0]):
                        combos.append(MNPuzzle(swap(origState, x, x+1, y, y),
                                               self.to_grid))
        return combos

    def is_solved(self):
        """
        Return whether MNPuzzle is solved. Solved when from_grid is the same as to_grid.

        @type self: MNPuzzle
        @rtype: bool

        >>> start_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> m = MNPuzzle(start_grid, target_grid)
        >>> m.is_solved()
        True

        >>> start_grid2 = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> m1 = MNPuzzle(start_grid2, target_grid2)
        >>> m1.is_solved()
        False
        """
        return self.from_grid == self.to_grid

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))

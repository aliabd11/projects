from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether SudokuPuzzle self is equivalent to other.

        @type self: SudokuPuzzle
        @type other: SudokuPuzzle | Any
        @rtype: bool

        >>> grid1 = [["*", "*", "*", "*"],\
                     ["*", "*", "*", "*"],\
                     ["*", "*", ".", "*"],\
                     ["*", "*", "*", "*"]]
        >>> s1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid3 = [["*", "*", "*", "*"],\
                     ["*", ".", "*", "*"],\
                     ["*", "*", "*", "*"],\
                     ["*", "*", "*", "*"]]
        >>> s3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> s1.__eq__(s3)
        False
        """
        return (type(other) == type(self) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitairePuzzle
        self.
​
        >>> grid = [\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", ".", "*", "*"],\
            ["*", "*", "*", "*", "*"]]
        >>> g = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(g)
        * * * * *
        * * * * *
        * * * * *
        * * . * *
        * * * * *
        """
        table = ""
        row_count = 0
        for row in self._marker:  # Goes through each row, makes a str table
            col_count = 0
            for i in row:
                if col_count < len(row)-1:
                    table += (i + " ")
                    col_count += 1
            if row_count < len(self._marker)-1:
                table += (i + '\n')
                row_count += 1
            else:
                table += i
        return table  # Returns str rep table of puzzle

    def extensions(self):
        """
        Returns all possible configurations that can be reached by making a
        single jump from this configuration
        @type: self: Puzzle
        @return: list[Puzzle]

        >>> list1 = [[".",".",".",".","."],\
                    [".",".","*","*","."],\
                    [".",".",".",".","."]]
        >>> list2 = [[".",".",".",".","."],\
                     [".","*",".",".","."],\
                     [".",".",".",".","."]]
        >>> list3 = [[".",".",".",".","."],\
                     [".",".",".",".","*"],\
                     [".",".",".",".","."]]
        >>> x = GridPegSolitairePuzzle(list1,{"*", ".", "#"})
        >>> a = x.extensions()
        >>> b = [GridPegSolitairePuzzle(list2,{"*", ".", "#"})\
               ,GridPegSolitairePuzzle(list3,{"*", ".", "#"})]
        >>> a == b
        True
        """
        def swap(marker, mx, x2, my, y2):
            """
            If proper conditions are met, jump over the peg depending on the
            condition
            @param marker: map, list of list
            @param mx: Original x coordinate
            @param x2: Replacement x coordinate
            @param my: Original y coordinate
            @param y2: Replacement y coordinate
            @return: list[list[str]]
            """
            # creates a deep copy
            # each if statement checks whether to move the piece N S E W by
            # comparing the current coordinates and the new coordinates
            map = [x[:] for x in marker]
            map[my][mx], map[y2][x2] = map[y2][x2], map[my][mx]
            if my < y2:
                map[my+1][mx] = "."
            elif my > y2:
                map[my-1][mx] = "."
            elif mx < x2:
                map[my][mx+1] = "."
            else:
                map[my][mx-1] = "."
            return map

        def legal_move(marker, x, y, direction):
            """
            Checks if there is a potential move at the direction of"."
            coordinate
            @param marker: map of the board
            @param x: x coordinate
            @param y: y coordinate
            @param direction : North South East West of the "."
            @return: boolean
            """
            # first if statement determines the directions
            # second if statement checks if the "potential move" is within the index
            if direction == "N":
                if 0 <= y-2 < len(marker):
                    return marker[y-2][x] == marker[y-1][x] == '*'
            if direction == "S":
                if 0 <= y+2 < len(marker):
                    return marker[y+2][x] == marker[y+1][x] == '*'
            if direction == "W":
                if 0 <= x-2 < len(marker[0]):
                    return marker[y][x-2] == marker[y][x-1] == '*'
            if direction == "E":
                if 0 <= x+2 < len(marker[0]):
                    return marker[y][x+2] == marker[y][x+1] == '*'
            return False

        combos = []
        # For loops go through the coordinates
        # each if statement checks and appends the new scenario
        # iff there is a legal move available
        for y in range(len(self._marker)):
            for x in range(len(self._marker[0])):
                if self._marker[y][x] == '.':
                    if legal_move(self._marker, x, y, 'N'):
                        combos.append(GridPegSolitairePuzzle(swap(self._marker,
                                            x, x, y, y-2), self._marker_set))
                    if legal_move(self._marker, x, y, 'S'):
                        combos.append(GridPegSolitairePuzzle(swap(self._marker,
                                            x, x, y, y+2), self._marker_set))
                    if legal_move(self._marker, x, y, 'W'):
                        combos.append(GridPegSolitairePuzzle(swap(self._marker,
                                            x, x-2, y, y), self._marker_set))
                    if legal_move(self._marker, x, y, 'E'):
                        combos.append(GridPegSolitairePuzzle(swap(self._marker,
                                            x, x+2, y, y), self._marker_set))
        return combos

    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.
        Solved when there is only one peg left.
        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = [["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", ".", "*", "*"],\
            ["*", "*", "*", "*", "*"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> s.is_solved()
        False

        >>> grid = [[".", ".", ".", ".", "."],\
            [".", ".", ".", ".", "."],\
            [".", ".", "*", ".", "."],\
            [".", ".", ".", ".", "."],\
            [".", ".", ".", ".", "."]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> s.is_solved()
        True
        """

        marker = self._marker
        amount_of_pegs = 0
        for row in marker:
            for i in row:
                if i == "*":
                    amount_of_pegs += 1
        return amount_of_pegs == 1

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
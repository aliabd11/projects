class Location:
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None

        >>> x = Location(6,7)
        >>> x.row == 6 and x.column == 7
        True
        """
        # TODO
        self.row = row
        self.column = column

    def __str__(self):
        """Return a string representation.

        @rtype: str

        >>> x = Location(6,7)
        >>> print(x)
        6, 7
        """
        # TODO
        return "{0}, {1}".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool

        >>> x = Location(6,7)
        >>> y = Location(6,7)
        >>> x == y
        True
        """
        # TODO
        if (self.row, self.column) == (other.row, other.column):
            return True
        else:
            return False


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int

    >>> x = Location(1,1)
    >>> y = Location(2,2)
    >>> manhattan_distance(x,y)
    2
    """
    # TODO
    return abs((destination.row - origin.row)) + abs((destination.column - origin.column))

def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location

    >>> x = "1,1"
    >>> y = deserialize_location(x)
    >>> isinstance(y, Location)
    True
    """
    # TODO
    return Location(int(location_str[0]), int(location_str[2])) #2 because location_str formatted as '6,7'

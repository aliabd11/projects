from location import Location

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """A rider for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the rider.
    @type origin: Location
        The origin of the rider.
    @type destination: Location
        The desired destination of the rider.
    @type patience: int
        The rider's patience.
    """

    # TODO
    def __init__(self, id, origin, destination, patience):
        """Initialize a Rider.

        @type self: Rider
        @type id: str
        @type origin: Location
        @type patience: int
        @type destination: Location
        @rtype: None

        >>> x = Rider("Bob", Location(6,6), Location(7,7), 8)
        >>> x.id == "Bob" and x.origin == Location(6,6) and x.destination == Location(7,7) and x.patience == 8
        True
        """

        self.id = id
        self.origin = origin
        self.patience = patience
        self.destination = destination
        self.status = WAITING

    def pickedup(self):
        """Rider status set to satisfied after being picked up.

        @type self: Rider
        @rtype: None
        >>> x = Rider("Bob", Location(6,6), Location(7,7), 8)
        >>> x.pickedup()
        >>> x.status == SATISFIED
        True
        """
        self.status = SATISFIED

    def __str__(self):
        """Return a string representation.

        @type self: Rider
        @rtype: str
        >>> x = Rider("Bob", Location(6,6), Location(7,7), 8)
        >>> print(x)
        Bob, 6, 6, waiting
        """
        # TODO
        return "{0}, {1}, {2}".format(self.id, self.origin, self.status)

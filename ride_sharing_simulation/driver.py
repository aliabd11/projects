from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type speed: int
        The speed of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed): #perhaps destination parameter
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None

        >>> x = Driver("100%csassignment", Location(1,1), 100)
        >>> x.identifier == "100%csassignment" and x.location == Location(1,1) and x.speed == 100
        True

        """
        # TODO
        self.identifier = identifier
        self.location = location
        self.speed = speed
        self.is_idle = True
        self.destination = None


    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str

        >>> x = Driver("100%csassignment", Location(1,1), 100)
        >>> print(x)
        100%csassignment, 1, 1, 100
        """
        # TODO
        return "{0}, {1}, {2}".format(self.identifier, self.location, self.speed)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver/
        @rtype: bool

        >>> x = Driver("king1", Location(1,1), 100)
        >>> z = Driver("king1", Location(2,3), 100)
        >>> z == x
        True

        >>> x = Driver("king3", Location(1,1), 100)
        >>> z = Driver("king1", Location(2,3), 100)
        >>> z == x
        False
        """
        # TODO
        if self.identifier == other.identifier:
            return True
        else:
            return False

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int

        >>> x = Driver("king1", Location(1,1), 1)
        >>> y = Location(6,7)
        >>> x.get_travel_time(y)
        11
        """
        # TODO
        return round(((abs(destination.row - self.location.row)) + (abs(destination.column - self.location.column))) / self.speed) #BECAUSE ROUNDED #PROBABLY WORKS #ABS VALUE NEEDED

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        >>> x = Driver("king1", Location(1,1), 1)
        >>> y = Location(9,8)
        >>> x.start_drive(y)
        15
        """
        # TODO
        self.idle = False
        return self.get_travel_time(location)


    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None. #

        @type self: Driver
        @rtype: None
        >>> x = Driver("king1", Location(1,1), 1)
        >>> x.is_idle = False
        >>> x.end_drive()
        >>> x.is_idle == True
        True
        """
        # TODO
        self.is_idle = True


    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> x = Driver("king1", Location(1,1), 1)
        >>> y = Rider("queen1", Location(8,9), Location(9,0), 9)
        >>> x.start_ride(y)
        9
        """
        # TODO
        rider.pickedup()
        return self.get_travel_time(rider.destination)


    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        >>> x = Driver("king1", Location(1,1), 1)
        >>> x.is_idle = False
        >>> x.end_ride()
        >>> x.is_idle == True
        True
        """
        # TODO
        self.is_idle = True
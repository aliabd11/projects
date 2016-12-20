"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location, manhattan_distance, Location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience, self.rider))
        return events


    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> x = Driver("Bob", Location(6,6), 8)
        >>> m = DriverRequest(6,x)
        >>> dispatch = Dispatcher()
        >>> monitor = Monitor()
        >>> z = m.do(dispatch, monitor)
        >>> isinstance(z, list)
        True
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        # TODO
        monitor.notify(self.timestamp, DRIVER, REQUEST, self.driver.identifier, self.driver.location)

        events = []
        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + abs(travel_time), rider, self.driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str

        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    # TODO
    def __init__(self, timestamp, rider):
        """Initialize a Cancellation event.

        @type self: Cancellation
        @type rider: Rider
        @rtype: None
        >>> z = Rider("Bob", Location(6,7), Location(8,7), 9)
        >>> x = Cancellation(6, z)
        >>> isinstance(x, Cancellation)
        True
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """If rider status is not SATISFIED, change it to CANCELLED,
        notify the monitor of a RIDER CANCEL event and cancel the ride

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None

        >>> z = Rider("Bob", Location(6,7), Location(8,7), 9)
        >>> x = Cancellation(6, z).do(Dispatcher(), Monitor())
        >>> x == None
        True
        """
        if self.rider.status != SATISFIED:
            self.rider.status = CANCELLED
            monitor.notify(self.timestamp, RIDER, CANCEL,
                       self.rider.id, self.rider.origin)
            dispatcher.cancel_ride(self.rider)

class Pickup(Event):
    # TODO
    def __init__(self, timestamp, rider, driver):
        """Initialize a Pickup event.

        @type self: Pickup
        @type driver: Driver
        @type rider: Rider
        @rtype: None

        >>> z = Rider("Bob", Location(6,7), Location(8,7), 9)
        >>> y = Driver("Bob", Location(6,6), 8)
        >>> x = Pickup(6, z, y)
        >>> isinstance(x, Pickup)
        True
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver
        self.driver.location = self.rider.origin

    def do(self, dispatcher, monitor):
        """Notify the monitor about a DRIVER PICKUP and RIDER PICKUP event.
        If rider status is CANCELLED, return a DriverRequest event and set driver destination to None.
        If rider status is WAITING, set driver destination to rider destination, return a Dropoff event
        and set rider status to SATISFIED

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None

        >>> z = Rider("Bob", Location(6,7), Location(8,7), 9)
        >>> y = Driver("Bob", Location(6,6), 8)
        >>> x = Pickup(6, z, y).do(Dispatcher(), Monitor())
        >>> isinstance(x, list)
        True
        """
        events = []
        monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.id, self.rider.origin)
        monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.identifier, self.driver.location)

        if self.rider.status == CANCELLED:
            events.append(DriverRequest(self.timestamp, self.driver))
            self.driver.destination = None
        elif self.rider.status == WAITING:
            self.driver.destination = self.rider.destination
            travel_time = self.driver.start_drive(self.rider.origin)
            drop_off_time = manhattan_distance(self.rider.origin, self.rider.destination) // self.driver.speed
            events.append(Dropoff(self.timestamp + abs(travel_time) + drop_off_time, self.rider, self.driver))
            self.rider.status = SATISFIED
        return events

class Dropoff(Event):
    # TODO
    def __init__(self, timestamp, rider, driver):
        """Initialize a Dropoff event.

        @type self: Pickup
        @type driver: Driver
        @type rider: Rider
        @rtype: None

        >>> z = Rider("Bob", Location(6,7), Location(8,7), 9)
        >>> y = Driver("Bob", Location(6,6), 8)
        >>> x = Dropoff(6, z, y)
        >>> isinstance(x, Dropoff)
        True
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver
        self.driver.location = self.rider.destination

    def do(self, dispatcher, monitor):
        """Notify the monitor about a DRIVER DROPOFF event and set rider status to SATISFIED
        Set Driver destination to none and return a DriverRequest event

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None

        >>> z = Rider("Bob", Location(6,7), Location(8,7), 9)
        >>> y = Driver("Bob", Location(6,6), 8)
        >>> x = Dropoff(6, z, y).do(Dispatcher(), Monitor())
        >>> isinstance(x, list)
        True
        """
        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.identifier, self.driver.location)

        events = []
        self.rider.status = SATISFIED
        events.append(DriverRequest(self.timestamp, self.driver))
        self.driver.destination = None
        return events


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]

    >>> x = create_event_list("events.txt")
    >>> isinstance(x, list)
    True
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            id = tokens[2]
            location = deserialize_location(tokens[3])

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                # TODO
                # Create a DriverRequest event.
                speed = int(tokens[4])

                driver = Driver(id, location, speed)
                event = DriverRequest(timestamp, driver)

            else:
                # TODO
                # Create a RiderRequest event.

                destination = deserialize_location(tokens[4])
                patience = int(tokens[5])

                rider = Rider(id, location, destination, patience)
                event = RiderRequest(timestamp, rider)

            events.append(event)
    return events

from driver import Driver
from rider import Rider
from location import Location, manhattan_distance

class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None

        >>> x = Dispatcher()
        >>> x.waitlist == [] and x.drivers == []
        True
        """
        # TODO
        self.waitlist = [] #waiting riders
        self.drivers = [] #available drivers

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str

        >>> x = Dispatcher()
        >>> print(x)
        Waiting list: [], Available drivers: []
        """
        return "Waiting list: {0}, Available drivers: {1}".format(self.waitlist, self.drivers)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None

        >>> z = Dispatcher()
        >>> y = Rider("TAIWANNUMBAONE", Location(8,9), Location(9,0), 9)
        >>> m = z.request_driver(y)
        >>> m == None
        True

        >>> z = Dispatcher()
        >>> y = Rider("TAIWANNUMBAONE", Location(8,9), Location(9,0), 9)
        >>> x = Driver("Bangock", Location(6,7), 6)
        >>> z.drivers.append(x)
        >>> m = z.request_driver(y)
        >>> isinstance(m, Driver)
        True

        """
        # TODO
        if not self.drivers:
            self.waitlist.append(rider)
            return None
        else:
            list_of_speeds = {} #dictionary with driver and speed of driver to rider origin
            for driver in self.drivers:
                list_of_speeds[(manhattan_distance(driver.location, rider.origin))] = driver
            driver = list_of_speeds[min(list_of_speeds)] #driver with fastest speed to rider
            self.drivers.remove(driver)
            return driver


    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None

        >>> z = Dispatcher()
        >>> x = Driver("Bangock", Location(6,7), 6)
        >>> m = z.request_rider(x)
        >>> m == None
        True

        >>> z = Dispatcher()
        >>> y = Rider("TAIWANNUMBAONE", Location(8,9), Location(9,0), 9)
        >>> z.waitlist.append(y)
        >>> x = Driver("Bangock", Location(6,7), 6)
        >>> m = z.request_rider(x)
        >>> isinstance(m, Rider)
        True

        """
        # TODO
        if not self.waitlist:
            if driver not in self.drivers:
                self.drivers.append(driver)
                return None
        else:
            return self.waitlist.pop(0) #rider waiting longest

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None

        >>> x = Dispatcher()
        >>> y = Rider("Amaranth", Location(6,7), Location(9,0), 9)
        >>> x.waitlist.append(y)
        >>> x.cancel_ride(y)
        >>> x.waitlist == []
        True

        """
        for waiting_rider in self.waitlist:
            if waiting_rider == rider:
                self.waitlist.remove(rider)
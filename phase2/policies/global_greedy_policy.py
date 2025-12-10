"""
Global greedy dispatch policy matching drivers to requests by distance.
"""
from .dispatch_policy import DispatchPolicy
from ..driver import Driver
from ..request import Request

class GlobalGreedyPolicy(DispatchPolicy):
    """
    Match drivers to requests by globally minimizing pickup distances.
    """

    def assign(self, drivers: list["Driver"], requests: list["Request"], time: int) -> list[tuple["Driver", "Request"]]:
        """
        Pair drivers and requests by iterating over combinations sorted by distance.

        Args:
            drivers (list[Driver]): Available drivers at the current tick.
            requests (list[Request]): Active requests waiting for assignment.
            time (int): Simulation tick (unused, kept for interface compatibility).

        Returns:
            list[tuple[Driver, Request]]: Greedy driver/request assignments.
        """
        combos = []
        for driver in drivers:
            for request in requests:
                distance = driver.position.distance_to(request.pickup)
                combos.append((distance, driver, request))

        combos.sort(key=lambda combo: (combo[0], getattr(combo[1], "id", 0), getattr(combo[2], "id", 0)))

        used_drivers = set()
        used_requests = set()
        matches = []

        for distance, driver, request in combos:
            if driver not in used_drivers and request not in used_requests:
                matches.append((driver, request))
                used_drivers.add(driver)
                used_requests.add(request)

        return matches
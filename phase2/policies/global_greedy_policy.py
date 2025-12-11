"""
Global greedy dispatch policy matching drivers to requests by distance.
"""
from .dispatch_policy import DispatchPolicy
from ..driver import Driver
from ..request import Request

class GlobalGreedyPolicy(DispatchPolicy):
    """
    Dispatch policy that considers all possible (driver, request) combinations
    and selects assignments using a global greedy strategy.

    The policy evaluates every driver–request pair, ranks them by distance
    from the driver’s current position to the request’s pickup location, and
    greedily assigns matches in ascending distance order while ensuring that
    each driver and each request is used at most once.
    """
    
    def assign(self, drivers: list["Driver"], requests: list["Request"], time: int) -> list[tuple["Driver", "Request"]]:
        """
        Assign drivers to requests using a global greedy matching strategy.

        Args:
            drivers (list[Driver]): The list of available drivers at the current simulation step.
            requests (list[Request]): The list of active requests waiting to be assigned.
            time (int): The current simulation time (not used directly but kept for interface compatibility).

        Returns:
            list[tuple[Driver, Request]]: A list of (driver, request) pairs selected by
            the global greedy matching process.
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
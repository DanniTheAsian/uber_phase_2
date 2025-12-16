"""
Global greedy dispatch policy.

This module implements a global greedy matching strategy which computes all
driver-request pairs, sorts them by driver-to-pickup distance and greedily
assigns the nearest available request to each driver.
"""

from .dispatch_policy import DispatchPolicy
from ..driver import Driver
from ..request import Request

class GlobalGreedyPolicy(DispatchPolicy):

    def assign(self, drivers: list["Driver"], requests: list["Request"], time: int) -> list[tuple["Driver", "Request"]]:
        """
        Assigns drivers to requests using a global greedy matching strategy.

        This method computes all possible (driver, request) combinations and 
        calculates the distance between each driver's current position and the 
        request's pickup location. All combinations are then sorted by distance 
        in ascending order.

        The algorithm selects matches greedily by iterating through the sorted 
        combinations and assigning each driver to the closest available request, 
        ensuring that no driver or request is assigned more than once.

        Args:
            drivers (list[Driver]): The list of available drivers at the current simulation step.
            requests (list[Request]): The list of active requests waiting to be assigned.
            time (int): The current simulation time (not used directly but kept for interface compatibility).

        Returns:
            list[tuple[Driver, Request]]: A list of (driver, request) pairs representing the assignments made.
        """
        combos = []
        
        for driver_index, driver in enumerate(drivers):
            if driver.status != "IDLE":
                continue
            for request in requests:
                try:
                    distance = driver.position.distance_to(request.pickup)
                except (AttributeError, TypeError, ValueError) as err:
                    print(f"Skipping driver/request pair due to distance error: {err}")
                    continue
               
                combos.append((distance, driver_index, driver, request))

        combos.sort()

        used_drivers = set()
        used_requests = set()
        matches = []

        for distance, _, driver, request in combos:
            if driver not in used_drivers and request not in used_requests:
                matches.append((driver, request))
                used_drivers.add(driver)
                used_requests.add(request)

        return matches
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
    """
    Global greedy dispatch strategy.

    At each simulation tick, the policy matches idle drivers to active
    requests by greedily selecting the closest available pairs.
    """
    def assign(self, drivers: list["Driver"], requests: list["Request"], time: int) -> list[tuple["Driver", "Request"]]:
        """
        Propose driver–request assignments for the current tick.

        All idle driver–request combinations are ranked by pickup distance,
        and matches are selected greedily so that each driver and request
        is used at most once.
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

        used_drivers_ids= set()
        used_requests_ids = set()
        matches = []

        for distance, _, driver, request in combos:
            if driver.id not in used_drivers_ids or request.id not in used_requests_ids:
                matches.append((driver, request))
                used_drivers_ids.add(driver.id)
                used_requests_ids.add(request.id)

        return matches
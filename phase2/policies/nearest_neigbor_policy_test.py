
    

"""
Nearest-neighbor dispatch policy.

This module implements a greedy nearest-neighbor matching policy which
repeatedly selects the closest (driver, request) pair among idle drivers
and waiting requests until no candidates remain.
"""

from .dispatch_policy import DispatchPolicy
from ..driver import Driver
from ..request import Request
from ..point import Point
class NearestNeighborPolicy(DispatchPolicy):

    def __init__ (self, cell_size: float = 5):
        self.cell_size = cell_size

    def _cell_of(self, point: Point) -> tuple[int, int]:
        return (
            int(point.x // self.cell_size),
            int(point.y // self.cell_size),
        )

    def assign(
    self,
    drivers: list[Driver],
    requests: list[Request],
    time: int
) -> list[tuple[Driver, Request]]:

        matches: list[tuple[Driver, Request]] = []

        grid: dict[tuple[int, int], list[Request]] = {}
        for request in requests:
            cell = self._cell_of(request.pickup)
            grid.setdefault(cell, []).append(request)

        idle_drivers = [d for d in drivers if d.status == "IDLE"]

        while idle_drivers and grid:
            best_pair = None
            best_distance = float("inf")

            for driver in idle_drivers:
                dcell = self._cell_of(driver.position)

                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        cell = (dcell[0] + dx, dcell[1] + dy)
                        for request in grid.get(cell, []):
                            dist = driver.position.distance_to(request.pickup)
                            if dist < best_distance:
                                best_distance = dist
                                best_pair = (driver, request)

            if best_pair is None:
                break

            driver, request = best_pair
            matches.append(best_pair)

            idle_drivers.remove(driver)
            rcell = self._cell_of(request.pickup)
            grid[rcell].remove(request)
            if not grid[rcell]:
                del grid[rcell]

        return matches

from phase2.policies.dispatch_policy import DispatchPolicy
from phase2.driver import Driver
from phase2.request import Request

class NearestNeighborPolicy(DispatchPolicy):
    """
    Assigns drivers to requests using a nearest-neighbor greedy strategy.

    This policy repeatedly selects the closest (driver, request) pair by scanning
    all idle drivers and all waiting requests, identifying the pair with the
    smallest distance between the driver’s current position and the request’s
    pickup location. Once the closest pair is found, both the driver and the
    request are removed from consideration to avoid multiple assignments.

    The process continues until either no idle drivers or no waiting requests
    remain.

    Arguments:
    drivers : list[Driver]
        The list of available drivers at the current simulation step.
    requests : list[Request]
        The list of active requests waiting to be assigned.
    time : int
        The current simulation time. This policy does not use the time
        parameter, but it is included to satisfy the DispatchPolicy interface.

    Return:
    list[tuple[Driver, Request]]
        A list of (driver, request) pairs selected by the nearest-neighbor
        matching process
    """
    def assign(self, drivers: list["Driver"], requests: list["Request"], time: int) -> list[tuple["Driver", "Request"]]:
        matches = []
    
        idle_drivers = drivers[:]
        waiting_requests = requests[:]

        while idle_drivers and waiting_requests:
            best_pair = None
            best_distance = float('inf')

            for driver in idle_drivers:
                for request in waiting_requests:
                    distance = driver.position.distance_to(request.pickup)
                    if distance < best_distance:
                        best_distance = distance
                        best_pair = (driver, request)
            
            if best_pair is None:
                break
                
            driver, request = best_pair
            matches.append(best_pair)

            idle_drivers.remove(driver)
            waiting_requests.remove(request)

        return matches
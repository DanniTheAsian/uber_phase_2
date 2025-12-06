from phase2.policies.dispatch_policy import DispatchPolicy

class NearestNeighborPolicy(DispatchPolicy):
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
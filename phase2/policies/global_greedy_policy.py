from phase2.policies.dispatch_policy import DispatchPolicy

class GlobalGreedyPolicy(DispatchPolicy):
    def assign(self, drivers: list["Driver"], requests: list["Request"], time: int) -> list[tuple["Driver", "Request"]]:
        combos = []
        for driver in drivers:
            for request in requests:
                distance = driver.position.distance_to(request.pickup)
                combos.append((distance, driver, request))

        combos.sort()

        used_drivers = set()
        used_requests = set()
        matches = []

        for distance, driver, request in combos:
            if driver not in used_drivers and request not in used_requests:
                matches.append((driver, request))
                used_drivers.add(driver)
                used_requests.add(request)

        return matches
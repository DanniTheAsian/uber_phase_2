from typing import Dict
from phase2.driver import Driver
from phase2.request import Request
from phase2.point import Point

from phase2.behaviour.lazy_behaviour import LazyBehaviour
from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.behaviour.earning_max_behaviour import EarningMaxBehaviour
from phase2.delivery_simulation import DeliverySimulation

class Translator:
    """
    Responsible ONLY for translating between
    GUI dictionaries and domain objects.
    """
    def driver_from_dict(self, driver: dict) -> Driver:
        """
        Convert a driver dictionary into a Driver object.

        Arguments
        ---------
        driver : dict
            Dictionary describing a driver from the GUI.

        Returns
        -------
        Driver
            A Driver domain object.
        """
        x = driver.get("x", 0.0)
        y = driver.get("y", 0.0)
        speed = driver.get("speed", driver.get("v", 1.0))
        driver_id = driver.get("id", driver.get("driver_id", 0))
        behaviour_type = (driver.get("behaviour", "")).lower()
        
        match behaviour_type:
            case "lazy":
                behaviour = LazyBehaviour()
            case "greedy" | "distance":
                behaviour = GreedyDistanceBehaviour()
            case "earn" | "earning" | "earning_max":
                behaviour = EarningMaxBehaviour()
            case _:
                behaviour = LazyBehaviour()

        status = driver.get("status","idle").upper()

        return Driver(id=driver_id, position=Point(x, y), speed=speed, behaviour=behaviour, status=status)
        
    def request_from_dict(self, request: Dict) -> Request:
        """
        Convert a request dictionary into a Request object.

        Arguments
        ---------
        request : dict
            Dictionary describing a request from the GUI.

        Returns
        -------
        Request
            A Request domain object.
        """
        rid = request.get("id", request.get("rid", request.get("req_id", 0)))
        px = request.get("px", request.get("x", 0))
        py = request.get("py", request.get("y", 0))
        dx = request.get("dx", request.get("tx", 0))
        dy = request.get("dy", request.get("ty", 0))
        t = request.get("t", 0)

        pickup = Point(px, py)
        dropoff = Point(dx, dy)

        return Request(id=rid, pickup=pickup, dropoff=dropoff, creation_time=t)


    def sim_to_state_dict(self, simulation: DeliverySimulation) -> Dict:
        """
        Convert the current simulation into a dictionary.

        Returns
        -------
        dict
            Dictionary representing the current simulation state.
        """
        drivers = []
        for driver in simulation.drivers:
            target = driver.target_point
            drivers.append({
                "id": driver.id,
                "x": float(driver.position.x),
                "y": float(driver.position.y),
                "status": driver.status.lower(),
                "request_id": driver.current_request.id if driver.current_request else None,
                "tx": float(target.x) if target else None,
                "ty": float(target.y) if target else None,
            })

        
        pending = []
        for request in simulation.requests:
            if request.status == "DELIVERED":
                continue

            pending.append({
                "id": request.id,
                "px": request.pickup.x,
                "py": request.pickup.y,
                "dx": request.dropoff.x,
                "dy": request.dropoff.y,
                "status": request.status.lower(),
                "t": request.creation_time
            })

        stats = {
            "served": simulation.served_count,
            "expired": simulation.expired_count,
            "avg_wait": (simulation.total_wait_time / simulation.completed_deliveries) if simulation.completed_deliveries else 0.0,
        }

        return {
            "t": simulation.time,
            "drivers": drivers,
            "pending": pending,
            "served": simulation.served_count,
            "expired": simulation.expired_count,
            "statistics": stats,
        }
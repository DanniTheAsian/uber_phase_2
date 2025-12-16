from typing import Dict, Tuple
from phase2.delivery_simulation import DeliverySimulation
from phase2.policies.global_greedy_policy import GlobalGreedyPolicy
from phase2.policies.nearest_neighbor_policy import NearestNeighborPolicy
from phase2.request_generator import RequestGenerator
from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request

from phase2.mutationrule.exploration import ExplorationMutationRule
from phase2.mutationrule.performance import PerformanceBasedMutation

from phase2.behaviour.lazy_behaviour import LazyBehaviour
from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.behaviour.earning_max_behaviour import EarningMaxBehaviour


class Adapter:
    """Adapter that maps the procedural dict API (UI) to phase2 objects.

    Responsibilities:
    - Convert input driver/request dicts into `Driver`/`Request` objects.
    - Create a `DeliverySimulation` with sensible defaults if not provided.
    - Expose `init_state` and `simulate_step` that work with the GUI's dict
      representation (keys used by `gui._engine`).
    """

    def __init__(self):
        self.simulation: DeliverySimulation | None = None
        self.next_request_id: int = 1


    def _driver_from_dict(self, driver: dict) -> Driver:
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
                behaviour = LazyBehaviour(min_wait_time=1)
            case "greedy" | "distance":
                behaviour = GreedyDistanceBehaviour(max_distance=10)
            case "earn" | "earning" | "earning_max":
                behaviour = EarningMaxBehaviour(min_ratio=0.1)
            case _:
                behaviour = LazyBehaviour(min_wait_time = 1)

        status = driver.get("status","idle").upper()

        return Driver(id=driver_id, position=Point(x, y), speed=speed, behaviour=behaviour, status=status)
              
    def _request_from_dict(self, request: Dict) -> Request:
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

    def _sim_to_state_dict(self) -> Dict:
        """
        Convert the current simulation into a dictionary.

        Returns
        -------
        dict
            Dictionary representing the current simulation state.
        """
        
        simulation = self.simulation
        assert simulation is not None

        drivers = []
        for driver in simulation.drivers:
            target = driver.target_point()

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
            status = request.status.lower()
            pending.append({
                "id": request.id,
                "px": request.pickup.x,
                "py": request.pickup.y,
                "dx": request.dropoff.x,
                "dy": request.dropoff.y,
                "status": "waiting" if status == "waiting" else ("assigned" if status == "assigned" else ("picked" if status == "picked" else status)),
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
    
    def init_state(self, drivers, requests,timeout, req_rate, width, height) -> Dict:
        """
        Initialize the simulation and return its initial state.

        Arguments
        ---------
        drivers : list[dict]
            Driver data from the GUI.
        requests : list[dict]
            Request data from the GUI.
        timeout : int
            Maximum waiting time for requests.
        req_rate : float
            Request generation rate.
        width : float
            Width of the simulation area.
        height : float
            Height of the simulation area.

        Returns
        -------
        dict
            Dictionary representing the initial simulation state.
        """
        driver_objects = [self._driver_from_dict(driver) for driver in drivers]
        request_objects = [self._request_from_dict(request) for request in requests]
    
        request_generator = RequestGenerator(rate=req_rate, width=width, height=height)

        dispatch_policy = NearestNeighborPolicy()
        mutation_rules = [
        ExplorationMutationRule(probability=0.5),
        PerformanceBasedMutation(threshold=0.3, N=5),
        ]

        self.simulation = DeliverySimulation(
            drivers= driver_objects,
            requests= request_objects,
            dispatch_policy=dispatch_policy,
            request_generator=request_generator,
            mutation_rules= mutation_rules,
            timeout=timeout,
        )

        return self._sim_to_state_dict()
    
    def simulate_step(self, _state) -> Tuple[Dict, Dict]:
        """
        Advance the simulation by one step.

        Arguments
        ---------
        _state : dict
            Previous state (required by the engine, not used).

        Returns
        -------
        tuple(dict, dict)
            Updated simulation state and statistics.
        """
        
        if self.simulation is None:
            raise RuntimeError("Simulation is not initialized")
        

        if self.simulation.expired_count > 50 and not isinstance(self.simulation.dispatch_policy, GlobalGreedyPolicy):
            self.simulation.dispatch_policy = GlobalGreedyPolicy()


        self.simulation.tick()
        new_state = self._sim_to_state_dict()
        metrics= new_state.get("statistics", {"served": 0, "expired": 0, "avg_wait": 0})
        return new_state, metrics

    def get_plot_data(self) -> dict:
        """
        Get plotting data for the GUI.

        Returns
        -------
        dict
            Data needed for visualizing drivers, requests, and statistics.
        """
        state = self._sim_to_state_dict()

        drivers = state["drivers"]
        pending= state["pending"]

        driver_positions = [(driver['x'], driver['y']) for driver in drivers]

        pickup_positions = [(request["px"], request["py"]) for request in pending
                            if request['status'] in {"WAITING", "ASSIGNED", "EXPIRED"}
                            ]
        
        dropoff_positions = [(request['dx'],request['dy']) for request in pending
                             if request["status"] == "PICKED"
                             ]
        driver_headings = [(driver['tx'] - driver['x'],
                            driver['ty'] - driver['y'])
                            if driver.get("tx") is not None and driver.get("y") is not None
                            else (0.0, 0.0)
                            for driver in drivers
                            ]
        return {
            "driver_positions": driver_positions,
            "pickup_positions": pickup_positions,
            "dropoff_positions": dropoff_positions,
            "driver_headings": driver_headings,
            "statistics": state.get("statistics", {}),
        }
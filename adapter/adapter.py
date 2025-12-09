from __future__ import annotations

from typing import Any, Dict

from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.behaviour.lazy_behaviour import LazyBehaviour
from phase2.delivery_simulation import DeliverySimulation
from phase2.driver import Driver
from phase2.point import Point
from phase2.policies.global_greedy_policy import GlobalGreedyPolicy
from phase2.request import Request
from phase2.request_generator import RequestGenerator
from phase2.mutationrule.exploration import ExplorationMutationRule


class SimulationAdapter:
    """Adapter class that connects the GUI with the DeliverySimulation backend."""

    ACTIVE_REQUEST_STATES = {"WAITING", "ASSIGNED", "PICKED"}

    def __init__(self) -> None:
        self.sim: DeliverySimulation | None = None
        self.request_generator: RequestGenerator | None = None
        self.dispatch_policy = GlobalGreedyPolicy()
        self.mutation_rule = ExplorationMutationRule(probability=0.05)
        self._next_driver_id = 0
        self._next_request_id = 1
        self._grid_width = 50
        self._grid_height = 30
        self._state_cache: Dict[str, Any] = {
            "t": 0,
            "drivers": [],
            "pending": [],
            "served": 0,
            "expired": 0,
        }

    # ------------------------------------------------------------------
    # Public API used by phase1 backend
    # ------------------------------------------------------------------
    def init_state(self, drivers, requests, timeout, req_rate, width, height):
        """Phase1 backend calls this."""
        self._grid_width = width
        self._grid_height = height
        self._next_driver_id = 0
        self._next_request_id = 1

        driver_objs = [self._driver_from_dict(d) for d in drivers]
        request_objs = [self._request_from_dict(r) for r in requests]

        self.request_generator = RequestGenerator(rate=req_rate, width=width, height=height)
        self.sim = DeliverySimulation(
            drivers=driver_objs,
            requests=request_objs,
            dispatch_policy=self.dispatch_policy,
            request_generator=self.request_generator,
            mutation_rule=self.mutation_rule,
            timeout=timeout,
        )

        self._state_cache = self._build_state_dict()
        return dict(self._state_cache)

    def simulate_step(self, state):
        """Phase1 backend calls this."""
        if self.sim is None:
            raise RuntimeError("Simulation not initialized")

        self.sim.tick()
        self._state_cache = self._build_state_dict()
        metrics = self._build_metrics()
        return dict(self._state_cache), metrics

    def get_plot_data(self):
        if self.sim is None:
            raise RuntimeError("Simulation not initialized")

        state = self._state_cache or self._build_state_dict()
        driver_positions = [(d["x"], d["y"]) for d in state.get("drivers", [])]
        driver_targets = [
            (d.get("tx"), d.get("ty")) for d in state.get("drivers", [])
        ]
        pickup_positions = [(r["px"], r["py"]) for r in state.get("pending", []) if r.get("status") in {"waiting", "assigned"}]
        dropoff_positions = [(r["dx"], r["dy"]) for r in state.get("pending", []) if r.get("status") == "picked"]

        return {
            "driver_positions": driver_positions,
            "driver_targets": driver_targets,
            "pickup_positions": pickup_positions,
            "dropoff_positions": dropoff_positions,
            "statistics": self._build_metrics(),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _driver_from_dict(self, data: Driver | Dict[str, Any]) -> Driver:
        if isinstance(data, Driver):
            self._next_driver_id = max(self._next_driver_id, data.id + 1)
            return data

        driver_id = int(data.get("id", self._next_driver_id))
        self._next_driver_id = max(self._next_driver_id, driver_id + 1)

        x = float(data.get("x", 0.0))
        y = float(data.get("y", 0.0))
        speed = float(data.get("speed", 1.0))
        behaviour = self._make_behaviour(data.get("behaviour"))

        status = str(data.get("status", "IDLE")).upper()
        if status not in {"IDLE", "TO_PICKUP", "TO_DROPOFF"}:
            status = "IDLE"

        return Driver(
            driver_id=driver_id,
            position=Point(x, y),
            speed=speed,
            behaviour=behaviour,
            status=status,
        )

    def _request_from_dict(self, data: Request | Dict[str, Any]) -> Request:
        if isinstance(data, Request):
            self._next_request_id = max(self._next_request_id, data.id + 1)
            return data

        request_id = int(data.get("id", self._next_request_id))
        self._next_request_id = max(self._next_request_id, request_id + 1)

        pickup = Point(float(data.get("px", data.get("pickup_x", 0.0))), float(data.get("py", data.get("pickup_y", 0.0))))
        dropoff = Point(float(data.get("dx", data.get("dropoff_x", 0.0))), float(data.get("dy", data.get("dropoff_y", 0.0))))
        creation_time = int(data.get("t", data.get("creation_time", 0)))

        req = Request(id=request_id, pickup=pickup, dropoff=dropoff, creation_time=creation_time)
        status = str(data.get("status", "waiting")).upper()
        req.status = status if status in {"WAITING", "ASSIGNED", "PICKED", "DELIVERED", "EXPIRED"} else "WAITING"
        req.wait_time = int(data.get("wait_time", data.get("wait", 0)))
        return req

    def _make_behaviour(self, descriptor: Any):
        name = str(descriptor).lower() if descriptor is not None else "lazy"
        if "greedy" in name:
            return GreedyDistanceBehaviour(max_distance=10.0)
        return LazyBehaviour(max_idle=5)

    def _build_state_dict(self) -> Dict[str, Any]:
        if self.sim is None:
            return dict(self._state_cache)

        drivers_state = [self._driver_to_dict(driver) for driver in self.sim.drivers]
        pending_requests = [
            self._request_to_dict(req)
            for req in self.sim.requests
            if req.status in self.ACTIVE_REQUEST_STATES
        ]

        state = {
            "t": self.sim.time,
            "drivers": drivers_state,
            "pending": pending_requests,
            "served": self.sim.served_count,
            "expired": self.sim.expired_count,
        }
        return state

    def _driver_to_dict(self, driver: Driver) -> Dict[str, Any]:
        target = driver.target_point()
        current_request_id = driver.current_request.id if driver.current_request else None
        return {
            "id": driver.id,
            "x": driver.position.x if driver.position else 0.0,
            "y": driver.position.y if driver.position else 0.0,
            "status": driver.status.lower(),
            "tx": target.x if target else None,
            "ty": target.y if target else None,
            "rid": current_request_id,
            "speed": driver.speed,
        }

    def _request_to_dict(self, request: Request) -> Dict[str, Any]:
        status_map = {
            "WAITING": "waiting",
            "ASSIGNED": "assigned",
            "PICKED": "picked",
            "DELIVERED": "delivered",
            "EXPIRED": "expired",
        }
        return {
            "id": request.id,
            "px": request.pickup.x,
            "py": request.pickup.y,
            "dx": request.dropoff.x,
            "dy": request.dropoff.y,
            "status": status_map.get(request.status, request.status.lower()),
            "t": request.creation_time,
            "wait": request.wait_time,
        }

    def _build_metrics(self) -> Dict[str, Any]:
        if self.sim is None:
            return {"served": 0, "expired": 0, "avg_wait": 0.0}

        avg_wait = (
            self.sim.total_wait_time / self.sim.completed_deliveries
            if self.sim.completed_deliveries
            else 0.0
        )
        return {
            "served": self.sim.served_count,
            "expired": self.sim.expired_count,
            "avg_wait": avg_wait,
        }

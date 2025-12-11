# adapter/adapter.py

from phase2.request_generator import RequestGenerator
from phase2.delivery_simulation import DeliverySimulation
from phase2.point import Point
from phase2.driver import Driver
from phase2.request import Request

from phase2.behaviour.lazy_behaviour import LazyBehaviour
from phase2.behaviour.greedy_distance_behaviour import GreedyDistanceBehaviour
from phase2.behaviour.earning_max_behaviour import EarningMaxBehaviour

from phase2.policies.nearest_neighbor_policy import NearestNeighborPolicy
from phase2.mutationrule.exploration import ExplorationMutationRule


class SimulationAdapter:
    """Adapter that maps the procedural dict API (UI) to phase2 objects.

    Responsibilities:
    - Convert input driver/request dicts into `Driver`/`Request` objects.
    - Create a `DeliverySimulation` with sensible defaults if not provided.
    - Expose `init_state` and `simulate_step` that work with the GUI's dict
      representation (keys used by `gui._engine`).
    """

    def __init__(self):
        self.sim: DeliverySimulation | None = None
        # request id counter stored on adapter instance to avoid module globals
        self.next_request_id: int = 1

    # --- Converters: dict -> objects ------------------------------------------------
    def _make_driver(self, driver: dict) -> Driver:
        x = float(driver.get("x", 0.0))
        y = float(driver.get("y", 0.0))
        speed = float(driver.get("speed", driver.get("v", 1.0)))
        bid = int(driver.get("id", driver.get("driver_id", 0)))

        behaviour_name = str(driver.get("behaviour", "lazy")).lower()
        if behaviour_name in ("lazy",):
            behaviour = LazyBehaviour(max_idle=5)
        elif behaviour_name in ("greedy", "distance"):
            behaviour = GreedyDistanceBehaviour(max_distance=10.0)
        elif behaviour_name in ("earning", "earn", "earning_max"):
            behaviour = EarningMaxBehaviour(min_ratio=1.0)
        else:
            behaviour = LazyBehaviour(max_idle= 5)

        status = str(driver.get("status", "idle")).upper()

        return Driver(id=bid, position=Point(x, y), speed=speed, behaviour=behaviour, status=status)

    def _make_request(self, r: dict) -> Request:
        rid = int(r.get("id", r.get("rid", r.get("req_id", 0))))
        px = float(r.get("px", r.get("x", 0.0)))
        py = float(r.get("py", r.get("y", 0.0)))
        dx = float(r.get("dx", r.get("tx", 0.0)))
        dy = float(r.get("dy", r.get("ty", 0.0)))
        t = int(r.get("t", 0))

        pickup = Point(px, py)
        dropoff = Point(dx, dy)
        return Request(id=rid, pickup=pickup, dropoff=dropoff, creation_time=t)

    # --- View builder: objects -> dict (UI friendly) --------------------------------
    def _state_from_sim(self) -> dict:
        sim = self.sim
        assert sim is not None

        drivers = []
        for driver in sim.drivers:
            target = driver.target_point()
            drivers.append({
                "id": driver.id,
                "x": float(driver.position.x),
                "y": float(driver.position.y),
                "status": str(driver.status).lower(),
                "rid": driver.current_request.id if driver.current_request else None,
                "tx": float(target.x) if target else None,
                "ty": float(target.y) if target else None,
            })

        pending = []
        for r in sim.requests:
            if not r.is_active():
                continue
            status = r.status.lower()
            pending.append({
                "id": r.id,
                "px": float(r.pickup.x),
                "py": float(r.pickup.y),
                "dx": float(r.dropoff.x),
                "dy": float(r.dropoff.y),
                "status": "waiting" if status == "waiting" else ("assigned" if status == "assigned" else ("picked" if status == "picked" else status)),
                "t": int(r.creation_time),
            })

        stats = {
            "served": sim.served_count,
            "expired": sim.expired_count,
            "avg_wait": (sim.total_wait_time / sim.completed_deliveries) if sim.completed_deliveries else 0.0,
        }

        return {
            "t": int(sim.time),
            "drivers": drivers,
            "pending": pending,
            "served": int(sim.served_count),
            "expired": int(sim.expired_count),
            "statistics": stats,
        }

    # --- Public adapter API ---------------------------------------------------------
    def init_state(self, drivers, requests, timeout, req_rate, width, height):
        """Initialize the `DeliverySimulation` from procedural backend inputs.

        Parameters expect lists of plain dicts (or None). Returns a state dict
        compatible with `gui._engine.AppSimState.sim`.
        """
        # convert to objects
        drivers_objs = [self._make_driver(driver) for driver in (drivers or [])]
        requests_objs = [self._make_request(r) for r in (requests or [])]

        request_gen = RequestGenerator(rate=req_rate, width=width, height=height)

        dispatch_policy = NearestNeighborPolicy()
        mutation_rule = ExplorationMutationRule(probability=0.01)

        self.sim = DeliverySimulation(
            drivers=drivers_objs,
            requests=requests_objs,
            dispatch_policy=dispatch_policy,
            request_generator=request_gen,
            mutation_rule=mutation_rule,
            timeout=timeout,
        )

        return self._state_from_sim()

    def simulate_step(self, state):
        """Advance the simulation one tick and return (new_state, metrics)."""
        if self.sim is None:
            raise RuntimeError("Simulation not initialized")

        self.sim.tick()
        new_state = self._state_from_sim()
        metrics = new_state.get("statistics", {"served": 0, "expired": 0, "avg_wait": 0.0})
        return new_state, metrics

    def get_plot_data(self):
        if self.sim is None:
            raise RuntimeError("Simulation not initialized")

        s = self._state_from_sim()
        driver_positions = [(d["x"], d["y"]) for d in s["drivers"]]
        pickup_positions = [(r["px"], r["py"]) for r in s["pending"] if r["status"] in ("waiting", "assigned")]
        dropoff_positions = [(r["dx"], r["dy"]) for r in s["pending"] if r["status"] == "picked"]

        # headings / quiver: use tx/ty if available
        driver_headings = []
        for d in s["drivers"]:
            if d.get("tx") is not None and d.get("ty") is not None:
                ux = d["tx"] - d["x"]
                uy = d["ty"] - d["y"]
            else:
                ux = 0.0
                uy = 0.0
            driver_headings.append((ux, uy))

        return {
            "driver_positions": driver_positions,
            "driver_headings": driver_headings,
            "pickup_positions": pickup_positions,
            "dropoff_positions": dropoff_positions,
            "statistics": s.get("statistics", {}),
        }

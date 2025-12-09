# adapter/adapter.py

from phase2.request_generator import RequestGenerator
from phase2.delivery_simulation import DeliverySimulation


class SimulationAdapter:
    """Adapter class that connects the GUI with the DeliverySimulation backend."""

    def __init__(self):
        self.sim = None

    def init_state(self, drivers, requests, timeout, req_rate, width, height):
        """Phase1 backend calls this."""
        print("INIT_STATE CALLED")  # <-- diagnostic

        request_gen = RequestGenerator(
            rate=req_rate,
            width=width,
            height=height
        )

        dispatch_policy = None
        mutation_rule = None

        self.sim = DeliverySimulation(
            drivers=drivers,
            requests=requests,
            dispatch_policy=dispatch_policy,
            request_generator=request_gen,
            mutation_rule=mutation_rule,
            timeout=timeout,
        )

        print("SIM CREATED:", self.sim)  # <-- diagnostic
        return {"t": 0}

    def simulate_step(self, state):
        """Phase1 backend calls this."""
        if self.sim is None:
            raise RuntimeError("Simulation not initialized")

        self.sim.tick()
        snapshot = self.sim.get_snapshot()

        state["t"] = self.sim.time
        metrics = snapshot["statistics"]
        return state, metrics

    def get_plot_data(self):
        if self.sim is None:
            raise RuntimeError("Simulation not initialized")

        snapshot = self.sim.get_snapshot()

        return {
            "driver_positions": snapshot["driver_positions"],
            "driver_headings": snapshot["driver_headings"],
            "pickup_positions": snapshot["pickup_positions"],
            "dropoff_positions": snapshot["dropoff_positions"],
            "statistics": snapshot["statistics"],
        }

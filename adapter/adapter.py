from phase2.delivery_simulation import DeliverySimulation

class SimulationAdapter:
    """Adapter class that connects the GUI with the DeliverySimulation backend."""

    def __init__(self):
        self.sim = None

    def init_state(self, drivers, requests, timeout, req_rate, width, height):
        """Phase1 backend calls this."""
        self.sim = DeliverySimulation(
            num_drivers=len(drivers),
            width=width,
            height=height,
            rate=req_rate,
            dispatch_policy=None,
            mutation_rule=None,
            timeout=timeout,
        )

        return {"t": 0}

    def simulate_step(self, state):
        """Phase1 backend calls this."""
        if self.sim is None:
            raise RuntimeError("Simulation not initialized")

        self.sim.tick()

        snapshot = self.sim.get_snapshot()

        # update Phase1 state dict
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

from phase2.delivery_simulation import DeliverySimulation

class SimulationAdapter:
    """ Adapter class that connects the GUI with the DeliverySimulation backend."""

    def __init__(self):
        self.sim = None

    def init_simulation(
        self,
        num_drivers: int,
        width: int,
        height: int,
        rate: float,
        dispatch_policy,
        mutation_rule,
        timeout: int,
    ) -> None:
        self.sim = DeliverySimulation(
            num_drivers=num_drivers,
            width=width,
            height=height,
            rate=rate,
            dispatch_policy=dispatch_policy,
            mutation_rule=mutation_rule,
            timeout=timeout,
        )

    
    def step_simulation(self) -> tuple[int, dict]:
        if self.sim is None:
            raise RuntimeError('simulation is not initialized')

        self.sim.tick()

        snapshot = self.sim.get_snapshot()
        current_time = self.sim.time
        statistics = snapshot['statistics']

        return current_time, statistics

    def get_ploy_data(self) -> dict:
        if self.sim is None:
            raise RuntimeError('simulation is not initialized')
        
        snapshot = self.sim.get_snapshot()

        return {
            "driver_positions": snapshot["driver_positions"],
            "driver_headings": snapshot["driver_headings"],
            "pickup_positions": snapshot["pickup_positions"],
            "dropoff_positions": snapshot["dropoff_positions"],
            "statistics": snapshot["statistics"],
        }

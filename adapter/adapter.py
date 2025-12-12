from typing import List, Dict, Tuple
from phase2.delivery_simulation import DeliverySimulation
from phase2.policies.nearest_neighbor_policy import NearestNeighborPolicy
from phase2.mutationrule.exploration import ExplorationMutationRule
from phase2.request_generator import RequestGenerator
from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request

class SimulationAdapter:
    def __init__(self) -> None:
        self.sim = None

    def init_state(self, drivers: list[Driver], requests: list[Request], timeout: int, req_rate: float, width: int, height: int) -> dict:
        print(f"DEBUG adapter.init_state: Received {len(requests)} requests")
        if requests:
            print(f"DEBUG adapter.init_state: First request type: {type(requests[0])}")

        dispatch_policy = NearestNeighborPolicy()
        mutation_rule = ExplorationMutationRule(0.1)
        request_generator = RequestGenerator(req_rate, width, height)

        self.sim = DeliverySimulation(drivers, requests, dispatch_policy, request_generator, mutation_rule, timeout)

        return {"t": 0}
    
    def simulation_step(self, state: Dict) -> Tuple[Dict, Dict]:

        if self.sim == None:
            raise RuntimeError("Simulation is not initialized.")
        
        self.sim.tick()
        snapshot = self.sim.get_snapshot()

        # DEBUG: Vis snapshot indhold
        print(f"\n=== ADAPTER SNAPSHOT ===")
        print(f"Snapshot keys: {snapshot.keys()}")
        print(f"driver_positions length: {len(snapshot.get('driver_positions', []))}")
        print(f"pickup_positions length: {len(snapshot.get('pickup_positions', []))}")
        print(f"dropoff_positions length: {len(snapshot.get('dropoff_positions', []))}")
        print("=======================\n")


        state["t"] = self.sim.time

        return state, snapshot["statistics"]
    
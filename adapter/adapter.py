from typing import Dict, Tuple
from phase2.delivery_simulation import DeliverySimulation
from phase2.policies.global_greedy_policy import GlobalGreedyPolicy
from phase2.policies.nearest_neighbor_policy import NearestNeighborPolicy
from phase2.request_generator import RequestGenerator

from phase2.mutationrule.exploration import ExplorationMutationRule
from phase2.mutationrule.performance import PerformanceBasedMutation

from .translator import Translator

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
        self.translator =  Translator()


  
    
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
        driver_objects = [self.translator.driver_from_dict(driver) for driver in drivers]
        request_objects = [self.translator.request_from_dict(request) for request in requests]
    
        request_generator = RequestGenerator(rate=req_rate, width=width, height=height)

        dispatch_policy = NearestNeighborPolicy()
        mutation_rules = [
        ExplorationMutationRule(probability=0.1),
        PerformanceBasedMutation(min_avg_earnings=0.3, N=5),
        ]

        self.simulation = DeliverySimulation(
            drivers= driver_objects,
            requests= request_objects,
            dispatch_policy=dispatch_policy,
            request_generator=request_generator,
            mutation_rules= mutation_rules,
            timeout=timeout,
        )

        return self.translator.sim_to_state_dict(self.simulation)
    
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
        
        simulation = self.simulation
        if simulation.expired_count > 50 and not isinstance(self.simulation.dispatch_policy, GlobalGreedyPolicy):
            simulation.dispatch_policy = GlobalGreedyPolicy()


        simulation.tick()
        state = self.translator.sim_to_state_dict(self.simulation)
        metrics= state.get("statistics", {"served": 0, "expired": 0, "avg_wait": 0})
        return state, metrics

    def get_plot_data(self) -> dict:
        """
        Get plotting data for the GUI.

        Returns
        -------
        dict
            Data needed for visualizing drivers, requests, and statistics.
        """
        assert self.simulation is not None
        state = self.translator.sim_to_state_dict(self.simulation)

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
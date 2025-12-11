from typing import List, Dict, Tuple, Optional
from .adapter import SimulationAdapter
from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request
from phase2.request_generator import RequestGenerator
import random



ADAPTER = SimulationAdapter()

def load_drivers(path):
    return []

def load_requests(path):
    return []

def generate_drivers(n: int, width: int, height: int) -> List[Driver]:
    drivers = []
    for i in range(n):
        speed = random.uniform(0.01, 1.0)
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        drivers.append(Driver(i, Point(x, y), speed))
    return drivers

def generate_requests(start_t: int, out_list: List[Dict], req_rate: float, width: int, height: int) -> None:

    request_generator = RequestGenerator(req_rate, width, height)
    new_requests = request_generator.maybe_generate(start_t)

    for request in new_requests:
        request_dict = {
            "id": request.id,
            "pickup": {"x": request.pickup.x, "y": request.pickup.y},
            "dropoff": {"x": request.dropoff.x, "y": request.dropoff.y},
            "creation_time": request.creation_time,
            "status": request.status
        }
        out_list.append(request_dict)

def init_state(drivers: List[Driver], requests: List[Request], timeout: int, req_rate: float, width: int, height: int) -> Dict:
    return ADAPTER.init_state(drivers, requests, timeout, req_rate, width, height)

def simulate_step(state: Dict) -> Tuple[Dict, Dict]:
    return ADAPTER.simulation_step(state)

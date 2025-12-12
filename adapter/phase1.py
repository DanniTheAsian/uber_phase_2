from .adapter import SimulationAdapter
from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request
from phase2.request_generator import RequestGenerator
import random

NUM_DRIVERS = 5
ADAPTER = SimulationAdapter()

def load_drivers(path):
    return []

def load_requests(path):
    return []

def generate_drivers(n: int, width: int, height: int) -> list[Driver]:
    drivers = []
    for i in range(n):
        speed = random.uniform(0.01, 1.0)
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        drivers.append(Driver(i, Point(x, y), speed))
    return drivers

def generate_requests(start_t: int, out_list: list[dict], req_rate: float, width: int, height: int) -> None:
    request_generator = RequestGenerator(req_rate, width, height)
    new_requests = request_generator.maybe_generate(start_t)

    for request in new_requests:
        out_list.append({
            "id": request.id,
            "pickup": {"x": request.pickup.x, "y": request.pickup.y},
            "dropoff": {"x": request.dropoff.x, "y": request.dropoff.y},
            "creation_time": request.creation_time,
            "status": request.status
        })

def init_state(drivers: list[Driver], requests: list[Request], timeout: int, req_rate: float, width: int, height: int) -> dict:
    print(f"=== PHASE1 init_state ===")
    print(f"Input: {len(drivers)} drivers, {len(requests)} request OBJECTS")
    
    # INGEN konvertering nødvendig - de er allerede Request objekter!
    print(f"First request type: {type(requests[0]) if requests else 'None'}")
    
    # Send direkte videre til adapter
    result = ADAPTER.init_state(drivers, requests, timeout, req_rate, width, height)
    print("=========================")
    return result

def simulate_step(state: dict) -> tuple[dict, dict]:
    return ADAPTER.simulation_step(state)

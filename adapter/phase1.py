from .adapter import Adapter
from phase2.driver import Driver
from phase2.point import Point
from phase2.request import Request
from phase2.request_generator import RequestGenerator
import random


ADAPTER = Adapter()

def load_drivers(path):
    return []

def load_requests(path):
    return []

def generate_drivers(n: int, width: int, height: int) -> list[Dict]:
    drivers = []
    for i in range(n):
        speed = random.uniform(0.01, 1.0)
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        driver = Driver(i, Point(x, y), speed, status="IDLE", behaviour=None)

        drivers.append(
            {"id": driver.id,
             "x": driver.position.x,
             "y": driver.position.y,
             "speed": driver.speed,
             "status": driver.status,
             "behavior": None
             }
        ) 

    return drivers

def generate_drivers(n, width, height):
    drivers: List[Dict] = []
    for i in range(n):
        speed = random.uniform(0.5, 1.5)
        drivers.append(
            {
                "id": i,
                "x": random.uniform(0, width),
                "y": random.uniform(0, height),
                "speed": speed,
                "status": "idle",
                "behaviour": "lazy",
            }
        )
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
    print(f"Input: {len(drivers)} drivers, {len(requests)} requests")
    print(f"First request type: {type(requests[0]) if requests else 'None'}")
    
    # KONVERTER dicts til Request objekter
    request_objects = []
    for req in requests:
        if isinstance(req, dict):
            # Konverter dict til Request
            request = Request(
                id=req["id"],
                pickup=Point(req["pickup"]["x"], req["pickup"]["y"]),
                dropoff=Point(req["dropoff"]["x"], req["dropoff"]["y"]),
                creation_time=req.get("creation_time", 0)
            )
            if "status" in req:
                request.status = req["status"]
            request_objects.append(request)
        else:
            request_objects.append(req)  # Allerede Request objekt
    
    print(f"Converted to {len(request_objects)} Request objects")
    print("=========================")
    result = ADAPTER.init_state(drivers, request_objects, timeout, req_rate, width, height)
    return result

def simulate_step(state: dict) -> tuple[dict, dict]:
    return ADAPTER.simulation_step(state)

def get_plot_data() -> dict:
    """Return data needed for plotting."""
    if ADAPTER.sim is None:
        raise RuntimeError("Simulation not initialized")
    
    snapshot = ADAPTER.sim.get_snapshot()
    
    print(f"\n=== GET_PLOT_DATA ===")
    print(f"Returning: {len(snapshot.get('driver_positions', []))} drivers")
    print("====================\n")
    
    return {
        "driver_positions": snapshot.get("driver_positions", []),
        "pickup_positions": snapshot.get("pickup_positions", []),
        "dropoff_positions": snapshot.get("dropoff_positions", []),
        "statistics": snapshot.get("statistics", {})
    }
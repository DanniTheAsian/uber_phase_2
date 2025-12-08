from adapter import SimulationAdapter

ADAPTER = SimulationAdapter()

def load_drivers(path):
    return []

def load_requests(path):
    return []

def generate_drivers(n, width, height):
    return [None] * n

def generate_requests(start_t, out_list, rate, width, height):
    pass

def init_state(drivers, requests, timeout, req_rate, width, height):
    return ADAPTER.init_state(
        drivers=drivers,
        requests=requests,
        timeout=timeout,
        req_rate=req_rate,
        width=width,
        height=height,
    )

def simulate_step(state):
    return ADAPTER.simulate_step(state)

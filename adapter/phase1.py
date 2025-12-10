from __future__ import annotations

import itertools
import random
from typing import Dict, List

from .adapter import SimulationAdapter


ADAPTER = SimulationAdapter()
_REQUEST_COUNTER = itertools.count(1)


def load_drivers(_path):
    return []


def load_requests(_path):
    return []


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


def generate_requests(start_t, out_list, rate, width, height):
    if rate <= 0:
        return

    whole = int(rate)
    fractional = rate - whole
    count = whole
    if random.random() < fractional:
        count += 1

    for _ in range(count):
        out_list.append(
            {
                "id": next(_REQUEST_COUNTER),
                "px": random.uniform(0, width),
                "py": random.uniform(0, height),
                "dx": random.uniform(0, width),
                "dy": random.uniform(0, height),
                "t": start_t,
                "status": "waiting",
            }
        )

def init_state(drivers, requests, timeout, req_rate, width, height):
    return ADAPTER.init_state(
        drivers=list(drivers or []),
        requests=list(requests or []),
        timeout=timeout,
        req_rate=req_rate,
        width=width,
        height=height,
    )

def simulate_step(state):
    return ADAPTER.simulate_step(state)

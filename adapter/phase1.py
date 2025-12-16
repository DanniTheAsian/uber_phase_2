"""
Utility functions for initializing and running the delivery simulation.

This module provides helper functions used by the GUI/engine to:
- generate initial driver and request data,
- initialize the simulation state via the Adapter,
- advance the simulation one step at a time.

The functions operate on dictionary-based data structures, which are
converted into domain objects inside the Adapter.
"""

import random
from typing import Dict, List
from adapter.adapter import Adapter


ADAPTER = Adapter()



def load_drivers(_path):
    return []


def load_requests(_path):
    return []


def generate_drivers(n, width, height):
    """
    Generate a list of driver dictionaries with random positions and speeds.

    Args:
        n (int): Number of drivers to generate.
        width (float): Width of the simulation area.
        height (float): Height of the simulation area.

    Returns:
        list[dict]: A list of driver dictionaries compatible with the Adapter.
    """
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
    """
    Generate new requests based on a request rate and append them to a list.

    The number of generated requests is determined by the rate parameter,
    where the fractional part represents the probability of generating
    one additional request.

    Args:
        start_t (int): Current simulation time.
        out_list (list): List to which new request dictionaries are appended.
        rate (float): Request generation rate per time step.
        width (float): Width of the simulation area.
        height (float): Height of the simulation area.
    """
    if rate <= 0:
        return

    count = int(rate)

    if random.random() < (rate - count):
        count += 1

    for _ in range(count):
        out_list.append({
            "id": ADAPTER.next_request_id,
            "px": random.uniform(0, width),
            "py": random.uniform(0, height),
            "dx": random.uniform(0, width),
            "dy": random.uniform(0, height),
            "t": start_t,
            "status": "waiting",
        })
        ADAPTER.next_request_id += 1

def init_state(drivers, requests, timeout, req_rate, width, height):
    """
    Initialize the simulation state using the Adapter.

    This function converts driver and request dictionaries into
    domain objects and returns the initial simulation state
    in dictionary form for the GUI.

    Args:
        drivers (list[dict]): Initial driver data.
        requests (list[dict]): Initial request data.
        timeout (int): Maximum waiting time before a request expires.
        req_rate (float): Request generation rate.
        width (float): Width of the simulation area.
        height (float): Height of the simulation area.

    Returns:
        dict: Initial simulation state.
    """
    return ADAPTER.init_state(
        drivers=list(drivers or []),
        requests=list(requests or []),
        timeout=timeout,
        req_rate=req_rate,
        width=width,
        height=height,
    )

def simulate_step(state):
    """
    Advance the simulation by one discrete time step.

    This function delegates the simulation logic to the Adapter
    and returns the updated state and performance metrics.

    Args:
        state (dict): Previous simulation state (required by the engine).

    Returns:
        tuple(dict, dict): Updated simulation state and statistics.
    """
    return ADAPTER.simulate_step(state)

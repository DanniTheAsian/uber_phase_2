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



def load_drivers(path:str) -> list[dict]:
    """
    Load driver records from a CSV file containing x,y coordinates.
    
    Args:
        path (str): Path to the CSV file with driver data
        
    Returns:
        list[dict]: List of driver dictionaries
    """
    drivers = []

    if not path.lower().endswith('.csv'):
        print("File must be a CSV file")
        return drivers
    try:
        with open(path,'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
        return drivers
    except OSError as e:
        print(f"Error: Could not read the file '{path}': {e}")
        return drivers
    except Exception as e:
        print(f"An unexpected error occurred while reading the file '{path}': {e}")
        return drivers

    data_line_count = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split(',')
        if len(parts) < 2:
            continue

        try:
            x = float(parts[0])
            y = float(parts[1])

            # validate data ranges
            if not 0 <= x <= 50 or not 0 <= y <= 30:
                print(f"Warning: Skipping driver - Coordinate with out-of-bounds location: {line}")
                continue  # Skip lines with out-of-bounds location

            # only increment for valid data lines
            data_line_count +=1

            drivers.append({
                'id': data_line_count,
                'x': x,
                'y': y,
                'vx': 0.0,
                'vy': 0.0,
                'speed': random.uniform(0.5, 2.0), # Default speed between 0.5 and 2.0
                'tx': None, # Default target position is current position
                'ty': None, 
                'target_id': None # No assigned request
            })

        except (ValueError, IndexError) as e:
            # TESTING
            print(f"Warning: Skipping invalid line {data_line_count}: {line} ({e})")
            continue  # Skip invalid lines

        # TESTING
        print(f"Successfully loaded {len(drivers)} drivers from {path}")
    return drivers

def load_requests(path:str) -> list[dict]:
    """
    Loads request data from a CSV file and returns a list of dictionaries representing each request.
    Args:
        path (str): The file path to the CSV file containing request data.
    Returns:
        list[dict]: A list of dictionaries, each representing a request with column names as keys.

    """
    requests = []

    if not path.lower().endswith('.csv'):
        print("File must be a CSV file")
        return requests
    try:
        with open(path ,'r', encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
        return requests
    except OSError as e :
        print(f"Error: Could not read the file '{path}': {e}")
        return requests
    except Exception as e:
        print(f"An unexpected error occurred while reading the file '{path}': {e}")
        return requests

    data_line_count = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Skip empty lines and comments

        parts = line.split(',')
        if len(parts) < 5:
            continue  # Skip lines that don't have enough data

        try:
            # parse values
            appearence_time = int(parts[0])
            px = float(parts[1])
            py = float(parts[2])
            dx = float(parts[3])
            dy = float(parts[4])

            # validate data ranges
            if appearence_time < 0:
                print(f"Warning: Skipping line {data_line_count}"
                        f"with negative appearance time: {line}"
                        )
                continue  # Skip lines with negative appearance time
            if not 0 <= px <= 50 or not 0 <= py <= 30:
                print(f"Warning: Skipping line {data_line_count}"
                        f"with out-of-bounds pickup location: {line}")
                continue  # Skip lines with out-of-bounds pickup location
            if not 0 <= dx <= 50 or not 0 <= dy <= 30:
                print(f"Warning: Skipping line {data_line_count}"
                        f"with out-of-bounds dropoff location: {line}")
                continue  # Skip lines with out-of-bounds dropoff location

            # only increment for valid data lines
            data_line_count +=1

            requests.append({
                'id': data_line_count,
                'px': float(parts[1]), 'py': float(parts[2]),
                'dx': float(parts[3]), 'dy': float(parts[4]),
                't': int(parts[0]),
                't_wait': 0,
                'status': 'waiting',
                'driver_id': None
            })

        except (ValueError, IndexError) as e:
            # TESTING
            print(f"Warning: Skipping invalid line {data_line_count}: {line} ({e})")
            continue # Skip invalid lines

        # TESTING
        print(f"Successfully loaded {len(requests)} requests from {path}")

    return requests


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

from .adapter import SimulationAdapter
from phase2.driver import Driver
from phase2.request import Request
from phase2.point import Point
from phase2.behaviour.driver_behaviour import DriverBehaviour
import random


ADAPTER = SimulationAdapter()

def load_drivers(path):
    return []

def load_requests(path):
    return []

def generate_drivers(n, width, height):
    drivers = []
    width = 50
    height = 30

    for i in range(n):
        speed = random.uniform(0.01, 1)
        x = random.uniform(0, width)
        y = random.uniform(0, height)

        drivers.append(Driver(i, Point(x,y), speed, behaviour=None))
    return drivers

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

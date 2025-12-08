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


import random
import math

class Driver:
    def __init__(self, id, x, y, speed=1.0):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.target = None

    def set_target(self, tx, ty):
        self.target = (tx, ty)

    def move(self):
        if self.target is None:
            return
        tx, ty = self.target
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist <= self.speed:
            self.x = tx
            self.y = ty
            self.target = None
        else:
            self.x += self.speed * dx/dist
            self.y += self.speed * dy/dist


class Request:
    def __init__(self, id, px, py, dx, dy, t):
        self.id = id
        self.px = px
        self.py = py
        self.dx = dx
        self.dy = dy
        self.t = t
        self.status = "waiting"
        self.driver_id = None


class Simulation:
    def __init__(self, drivers, requests, timeout, rate, width, height):
        self.t = 0
        self.drivers = drivers
        self.pending = requests
        self.future = []
        self.served = 0
        self.expired = 0
        self.timeout = timeout
        self.served_waits = []
        self.rate = rate
        self.width = width
        self.height = height

    def generate_requests(self):
        if random.random() < self.rate:
            rid = "r" + str(self.t) + "_" + str(random.randint(0, 999))
            px = random.uniform(0, self.width)
            py = random.uniform(0, self.height)
            dx = random.uniform(0, self.width)
            dy = random.uniform(0, self.height)
            self.pending.append(Request(rid, px, py, dx, dy, self.t))

    def assign(self):
        for req in self.pending:
            if req.status == "waiting":
                for d in self.drivers:
                    if d.target is None:
                        d.set_target(req.px, req.py)
                        req.status = "assigned"
                        req.driver_id = d.id
                        break

    def step(self):
        self.t += 1
        self.generate_requests()
        self.assign()
        for d in self.drivers:
            d.move()
        return self

import matplotlib.pyplot as plt

def plot_cumulative_requests_over_time(simulation, max_time = 600):
    """
    Plots cumulative served and expired requests over time from a DeliverySimulation instance.
    X-axis: time
    Y-axis: cumulative requests (served and expired)
    """
    # The metrics log collected during simulation
    if not hasattr(simulation, 'metrics_log') or not simulation.metrics_log:
        print("No metrics_log available from the Simulation")
        return

    times = [entry['time'] for entry in simulation.metrics_log]
    served = [entry['served'] for entry in simulation.metrics_log]
    expired = [entry['expired'] for entry in simulation.metrics_log]

    plt.figure(figsize=(10, 6))
    plt.plot(times, served, label="Served Requests", color="green")
    plt.plot(times, expired, label="Expired Requests", color="red")
    plt.xlabel("Time (ticks)")
    plt.ylabel("Cumulative Requests")
    plt.title("Cumulative Served and Expired Requests Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()




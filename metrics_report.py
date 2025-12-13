
import matplotlib.pyplot as plt

def plot_cumulative_requests_over_time(simulation, max_time = 600) -> None:
    """
    Plots cumulative served and expired requests over time from a DeliverySimulation instance.
    X-axis: time
    Y-axis: cumulative requests (served and expired)
    
    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (optional)
    """

    # The metrics log collected during simulation
    if not hasattr(simulation, 'metrics_log') or not simulation.metrics_log:
        print("No metrics_log available from the simulation")
        return
    
     # Filter data based on max_time
    filtered_log = []
    for entry in simulation.metrics_log:
        if entry['time'] <= max_time:
            filtered_log.append(entry)

    if len(filtered_log) == 0:
        print(f"No data within time range 0-{max_time}")
        return

    times = []
    served = []
    expired = []

    skipped_entries = 0

    for entry in filtered_log:
        try:
            time_value = entry['time']
            served_value = entry['served']
            expired_value = entry['expired']

            times.append(time_value)
            served.append(served_value)
            expired.append(expired_value)

        except KeyError as e:
            print(f"Skipping entry due to missing key: {e}")
            skipped_entries += 1
            continue

    if skipped_entries > 0:
        print(f"Warning: Skipped {skipped_entries} entries due to missing data")

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


if __name__ == "__main__":
    """
    Test section for the plot function.
    This code only runs when the file is executed directly,
    not when it's imported as a module.
    """
    
    print("Testing metrics_report.py...")
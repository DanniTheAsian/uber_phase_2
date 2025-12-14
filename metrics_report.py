from typing import List, Dict, Optional, Tuple, Any
import matplotlib.pyplot as plt


def show_simulation_dashboard(simulation: Any, max_time: int = 600) -> None:
    """
    Displays the simulation dashboard with key metrics plots.

    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (in ticks)

    Returns:
        None: Displays matplotlib plots
    """
    plot_cumulative_requests_over_time(simulation, max_time)
    plot_average_wait_time(simulation, max_time)

def plot_cumulative_requests_over_time(simulation: Any, max_time: int = 600) -> None:
    """
    Plots cumulative served and expired requests over time.
    
    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (in ticks)
    
    Returns:
        None: Displays a matplotlib plot
    """

    # Step 1: Check if simulation has data
    has_data, error = check_simulation_has_data(simulation)
    if not has_data:
        print(f"Error: {error}")
        return
    
    # Step 2: Filter by time
    time_filtered = filter_by_time(simulation.metrics_log, max_time)
    
    if len(time_filtered) == 0:
        print(f"No data within time 0-{max_time}")
        return
    
    # Step 3: Filter by required keys
    data = filter_by_keys(time_filtered, ['time', 'served', 'expired'])
    
    if len(data) == 0:
        print("No entries have time, served, and expired keys")
        return
    
    # Step 4: Extract data for plotting
    times: List[int] = []
    served: List[int] = []
    expired: List[int] = []
    
    for entry in data:
        times.append(entry['time'])
        served.append(entry['served'])
        expired.append(entry['expired'])
    
    # Step 5: Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(times, served, label="Served Requests", color="green", linewidth=2)
    plt.plot(times, expired, label="Expired Requests", color="red", linewidth=2)
    plt.xlabel("Time (ticks)")
    plt.ylabel("Cumulative Requests")
    plt.title("Cumulative Served and Expired Requests Over Time")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()



def plot_average_wait_time(simulation: Any, max_time: int = 600) -> None:
    """
    Plots average wait time over time.

    Shows how long requests typically wait before being served.

    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (in ticks)

    Returns:
        None: Displays a matplotlib plot
    """
    # Step 1: Check if simulation has data
    has_data, error = check_simulation_has_data(simulation)
    if not has_data:
        print(f"Error: {error}")
        return

    # Step 2: Filter by time
    time_filtered = filter_by_time(simulation.metrics_log, max_time)

    if len(time_filtered) == 0:
        print(f"No data within time 0-{max_time}")
        return

    # Step 3: Filter by required keys - we need 'time' and 'avg_wait'
    data = filter_by_keys(time_filtered, ['time', 'avg_wait'])

    if len(data) == 0:
        print("No entries have both time and avg_wait keys")
        return

    # Step 4: Extract data for plotting
    times = []
    avg_waits = []

    for entry in data:
        times.append(entry['time'])
        avg_waits.append(entry['avg_wait'])

    # Step 5: Calculate overall average (for the red line)
    overall_average = 0.0
    if len(avg_waits) > 0:
        total = 0.0
        for wait_time in avg_waits:
            total += wait_time
        overall_average = total / len(avg_waits)

    # Step 6: Create the plot
    plt.figure(figsize=(10, 6))

    # Plot the average wait time as a blue line
    plt.plot(times, avg_waits, label="Average Wait Time", color="blue", linewidth=2)

    # Add a horizontal red dashed line for the overall average
    if len(avg_waits) > 0:
        plt.axhline(y = overall_average, color = "red", linestyle = "--",
                    label = f"Overall Average: {overall_average:.1f} ticks")

    # Add labels and title
    plt.xlabel("Time (ticks)")
    plt.ylabel("Average Wait Time (ticks)")
    plt.title("Average Request Wait Time Over Time")

    # Add legend and grid
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()

def check_simulation_has_data(simulation: Any) -> Tuple[bool, Optional[str]]:
    """ 
    Check if simulation has metrics data.
    
    Args:
        simulation: DeliverySimulation instance

    Returns:
        Tuple of (has_data: bool, error_msg: Optional[str])
    """
    if not hasattr(simulation, 'metrics_log'):
        return False, "Simulation has no metrics_log"
    
    if simulation.metrics_log is None or len(simulation.metrics_log) == 0:
        return False, "Metrics log is empty"
    
    return True, None

def filter_by_time(metrics_log, max_time) -> List[Dict]:
    """
    Filter metrics by time.
    
    Args:
        metrics_log: List of metric entries (dictionaries)
        max_time: Maximum time to include
    
    Returns:
        List of entries where time <= max_time
    """
    filtered = []
    for entry in metrics_log:
        try:
            if entry['time'] <= max_time:
                filtered.append(entry)
        except KeyError:
            continue  # Skip entries without 'time' key
    return filtered

def filter_by_keys(data: List[Dict], required_keys: Optional[List[str]]) -> List[Dict]:
    """
    Keep only entries that have all required keys.
    
    Args:
        data: List of metric entries
        required_keys: List of keys that must be present, or None for no filtering
    
    Returns:
        Filtered list containing only entries with all required keys
    """
    if required_keys is None:
        return data
    
    filtered = []
    for entry in data:
        has_all = True
        for key in required_keys:
            if key not in entry:
                has_all = False
                break
        
        if has_all:
            filtered.append(entry)
    
    return filtered


if __name__ == "__main__":
    """
    Test section for the plot function.
    This code only runs when the file is executed directly,
    not when it's imported as a module.
    """
    
    print("Testing metrics_report.py...")
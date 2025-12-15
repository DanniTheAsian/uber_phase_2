from typing import List, Dict, Optional, Tuple, Any
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def show_simulation_dashboard(simulation: Any, max_time: int = 600) -> None:
    """
    Displays the simulation dashboard with key metrics plots.

    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (in ticks)

    Returns:
        None: Displays matplotlib plots
    """
    # A figure with 3 subplots (vertical stack)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), sharex=True)
    
    # Plot
    plot_cumulative_requests_over_time(simulation, max_time, axes[0, 0])
    plot_average_wait_time(simulation, max_time, axes[0, 1])
    plot_driver_utilization(simulation, max_time, axes[1, 0])
    plot_behaviour_evolution(simulation, max_time, axes[1, 1])
    
    plt.tight_layout()
    plt.show()


def plot_cumulative_requests_over_time(simulation: Any, max_time: int = 600, ax: Optional[Axes] = None) -> Optional[Axes]:
    """
    Gets data for cumulative requests plot.
    
    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (in ticks)
        ax: Matplotlib axis to plot on. If None, creates new figure.
    
    Returns:
        Axes or None: The axis object if plot was created, None if no data
    """

    # Get valid data
    data = get_plot_data(simulation, max_time, ['time', 'served', 'expired'])
    if data is None:
        return None
    
    # Extract data
    times = []
    served = []
    expired = []
    
    for entry in data:
        times.append(entry['time'])
        served.append(entry['served'])
        expired.append(entry['expired'])
    
    # Create plot
    ax = create_base_plot("Cumulative Served and Expired Requests Over Time", "", "Cumulative Requests", ax)

    ax.plot(times, served, label="Served Requests", color="green", linewidth=2)
    ax.plot(times, expired, label="Expired Requests", color="red", linewidth=2)
    ax.legend()
    if ax is None:
        plt.tight_layout()
        plt.show()
    
    return ax



def plot_average_wait_time(simulation: Any, max_time: int = 600, ax: Optional[Axes] = None) -> Optional[Axes]:
    """
    Plots average wait time over time.
    
    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (in ticks)
        ax: Matplotlib axis to plot on. If None, creates new figure.
    
    Returns:
        Axes or None: The axis object if plot was created, None if no data
    """
    # Get valid data
    data = get_plot_data(simulation, max_time, ['time', 'avg_wait'])
    if data is None:
        return None

    # Extract data
    times = []
    avg_waits = []

    for entry in data:
        times.append(entry['time'])
        avg_waits.append(entry['avg_wait'])

    # Calculate overall average (Red line)
    overall_average = 0.0
    if len(avg_waits) > 0:
        total = 0.0
        for wait_time in avg_waits:
            total += wait_time
        overall_average = total / len(avg_waits)

    # Create plot
    ax = create_base_plot("Average Request Wait Time Over Time", "", "Average Wait Time (ticks)", ax)

    # Blue line for the average wait time over time
    ax.plot(times, avg_waits, label="Average Wait Time", color="blue", linewidth=2)

    # A horizontal red dashed line for the overall average
    if len(avg_waits) > 0:
        ax.axhline(y = overall_average, color = "red", linestyle = "--", label = f"Overall Average: {overall_average:.1f} ticks")

    ax.legend()

    if ax is None:
        plt.tight_layout()
        plt.show()
   
    return ax


def plot_driver_utilization(simulation: Any, max_time: int = 600, ax: Optional[Axes] = None) -> Optional[Axes]:
    """
    Plots driver utilization over time (active vs idle drivers).
    
    Shows how many drivers are working vs idle over time.
    
    Args:
        simulation: DeliverySimulation instance with metrics_log attribute
        max_time: Maximum time to display on x-axis (in ticks)
    
    Returns:
        Axes or None: The axis object if plot was created, None if no data
    """
    # Get valid data
    data = get_plot_data(simulation, max_time, ['time', 'active_drivers'])
    if data is None:
        return None
    
    # Extract data
    times = []
    active_counts = []
    
    for entry in data:
        times.append(entry['time'])
        active_counts.append(entry['active_drivers'])
    
    # Calculate idle drivers
    total_drivers = len(simulation.drivers)
    idle_counts = []
    for active in active_counts:
        idle = total_drivers - active
        idle_counts.append(idle)
    
    # Create plot
    ax = create_base_plot("Driver Utilization Over Time", "Time (ticks)", "Number of Drivers", ax)
    
    ax.stackplot(times, active_counts, idle_counts, labels=['Active Drivers', 'Idle Drivers'], colors=['blue', 'orange'], alpha = 0.7)
    ax.legend(loc='upper left')
    if ax is None:
        plt.tight_layout()
        plt.show()
    
    return ax


def plot_behaviour_evolution(simulation: Any, max_time: int = 600, ax: Optional[Axes] = None) -> Optional[Axes]:
    """
    Plots how driver behaviours change over time.
    
    Shows how many drivers have each behaviour type at each time step.
    """
    # Get valid data
    data = get_plot_data(simulation, max_time, ['time', 'behaviour_counts'])
    if data is None:
        return None
    
    # Find all different behaviour types that appear
    all_behaviour_types = set()
    for entry in data:
        if 'behaviour_counts' in entry:
            # Add all behaviour names from this time step
            for behaviour_name in entry['behaviour_counts'].keys():
                all_behaviour_types.add(behaviour_name)
    
    if not all_behaviour_types:
        print("Warning: No behaviour data to plot")
        return None
    
    # Prepare lists for plotting
    times = []
    # Create a dictionary to store counts for each behaviour type
    behaviour_data = {}
    for behaviour_name in all_behaviour_types:
        behaviour_data[behaviour_name] = []
    
    # Fill the data
    for entry in data:
        times.append(entry['time'])
        current_counts = entry.get('behaviour_counts', {})
        
        # For each behaviour type, add its count or 0
        for behaviour_name in all_behaviour_types:
            count = current_counts.get(behaviour_name, 0)
            behaviour_data[behaviour_name].append(count)
    
    # Create the plot
    ax = create_base_plot("Driver Behaviour Evolution", "Time (ticks)", "Number of Drivers", ax)
    
    # Colors for different lines
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']
    
    # Draw a line for each behaviour type
    for i, (behaviour_name, counts) in enumerate(behaviour_data.items()):
        color = colors[i % len(colors)]
        ax.plot(times, counts, 
                label=behaviour_name, 
                color=color, 
                linewidth=2)
    
    ax.legend(loc='best')  # Automatic best position for legend
    ax.grid(True, alpha=0.3)
    
    return ax


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

def filter_by_time(metrics_log: List[Dict], max_time: int) -> List[Dict]:
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

def filter_by_keys(data: List[Dict], required_keys: List[str]) -> List[Dict]:
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

def get_plot_data(simulation: Any, max_time: int, required_keys: List[str]) -> Optional[List[Dict]]:
    """
    Get validated and filtered data for plotting.
    
    Args:
        simulation: DeliverySimulation instance with metrics_log
        max_time: Maximum time to include (in ticks)
        required_keys: List of keys that must be present in each entry
        
    Returns:
        Filtered list of metric entries, or None if validation fails
    """

    # Step 1
    has_data, error = check_simulation_has_data(simulation)
    if not has_data:
        print(f"Error: {error}")
        return None
    
    # Step 2
    time_filtered = filter_by_time(simulation.metrics_log, max_time)
    if len(time_filtered) == 0:
        print(f"No data within time 0-{max_time}")
        return None
    
    # Step 3
    data = filter_by_keys(time_filtered, required_keys)
    if len(data) == 0:
        print(f"No entries have all required keys: {required_keys}")
        return None
    
    return data

def create_base_plot(title: str, xlabel: str, ylabel: str, ax: Optional[Axes] = None) -> Axes:
    """
    Create a base plot with consistent formatting.
    
    Args:
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        ax: Matplotlib axis. If None, creates new figure.
    
    Returns:
        Axes: The axis object to plot on
    """
    if ax is None:
        plt.figure(figsize=(10, 6))
        ax = plt.gca()
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    return ax


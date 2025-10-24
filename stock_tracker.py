"""
Single-module application to track the performance of a base stock
and its 2x leveraged version over 100 daily ticks.
"""

import random
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# Global constants
MEAN_DAILY_CHANGE = 0.0002  # 0.02%
STDEV_DAILY_CHANGE = 0.06   # 6.0%
INITIAL_VALUE = 1000.0
NUM_TICKS = 100


def generate_daily_change():
    """
    Generate a random daily change using a normal distribution.

    Returns:
        float: The daily change as a decimal (e.g., 0.03 for 3%)
    """
    return random.gauss(MEAN_DAILY_CHANGE, STDEV_DAILY_CHANGE)


def apply_change(value, change):
    """
    Apply a percentage change to a value.

    Args:
        value (float): The current value
        change (float): The percentage change as a decimal (e.g., 0.03 for 3%)

    Returns:
        float: The new value after applying the change
    """
    return value * (1 + change)


def run_simulation(seed=None, verbose=True):
    """
    Run the stock tracking simulation for NUM_TICKS days.

    Args:
        seed (int, optional): Random seed for reproducibility. If None, uses a random seed.
        verbose (bool): If True, print tick-by-tick results. Default is True.

    Returns:
        list: List of tuples (tick_number, daily_change, base_value, leveraged_value)
    """
    # Set up random seed
    if seed is None:
        seed = random.randint(0, 999999)
    random.seed(seed)

    if verbose:
        print(f"Random seed: {seed}\n")

    # Initialize stock values
    base_value = INITIAL_VALUE
    leveraged_value = INITIAL_VALUE

    results = []

    # Run simulation for NUM_TICKS days
    for tick in range(1, NUM_TICKS + 1):
        # Generate daily change
        daily_change = generate_daily_change()

        # Apply change to base stock
        base_value = apply_change(base_value, daily_change)

        # Apply 2x change to leveraged stock
        leveraged_change = daily_change * 2
        leveraged_value = apply_change(leveraged_value, leveraged_change)

        # Store results
        results.append((tick, daily_change, base_value, leveraged_value))

        # Print tick results if verbose
        if verbose:
            print(f"({tick}, {daily_change * 100:.2f}%, {base_value:.2f}, {leveraged_value:.2f})")

    return results


def calculate_difference_trajectory(results):
    """
    Calculate the difference between leveraged and base stock values over time.

    Args:
        results (list): List of tuples from run_simulation

    Returns:
        list: List of differences [0, diff_after_tick1, diff_after_tick2, ...]
              where difference = leveraged_value - base_value
    """
    # Start at 0 difference (tick 0, before any changes)
    differences = [0.0]

    for tick, daily_change, base_value, leveraged_value in results:
        difference = leveraged_value - base_value
        differences.append(difference)

    return differences


def run_multiple_simulations(num_runs=500, verbose=False):
    """
    Run multiple simulations and collect difference trajectories.

    Args:
        num_runs (int): Number of simulation runs to perform. Default is 500.
        verbose (bool): If True, print progress updates. Default is False.

    Returns:
        list: List of difference trajectories, one per run
    """
    all_trajectories = []

    for run_num in range(num_runs):
        if verbose and (run_num + 1) % 10 == 0:
            print(f"Completed {run_num + 1}/{num_runs} runs...")

        # Run simulation without verbose output
        results = run_simulation(seed=None, verbose=False)

        # Calculate difference trajectory
        trajectory = calculate_difference_trajectory(results)
        all_trajectories.append(trajectory)

    return all_trajectories


def plot_difference_trajectories(trajectories, filename="multiple_runs.png"):
    """
    Plot all difference trajectories on a single graph.

    Args:
        trajectories (list): List of difference trajectories
        filename (str): Output filename for the plot. Default is "multiple_runs.png"
    """
    plt.figure(figsize=(12, 8))

    # X-axis is ticks 0 through NUM_TICKS
    x_values = list(range(NUM_TICKS + 1))

    # Plot each trajectory
    for trajectory in trajectories:
        plt.plot(x_values, trajectory, alpha=0.3, linewidth=0.8)

    # Add reference line at y=0
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

    plt.xlabel('Tick Number')
    plt.ylabel('Difference (Leveraged - Base)')
    plt.title(f'Leveraged vs Base Stock Performance\n({len(trajectories)} runs, {NUM_TICKS} ticks each)')
    plt.grid(True, alpha=0.3)

    # Save the plot
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to {filename}")

    # Display the plot
    plt.show()


def main():
    """
    Main entry point for the application.
    Run a single simulation with verbose output.
    """
    run_simulation()


def calculate_summary_statistics(trajectories):
    """
    Calculate summary statistics for final values across all trajectories.

    Args:
        trajectories (list): List of difference trajectories

    Returns:
        dict: Dictionary containing mean, std, skew, and kurtosis
    """
    # Extract final values (last element of each trajectory)
    final_values = [trajectory[-1] for trajectory in trajectories]

    # Calculate statistics
    mean = np.mean(final_values)
    std = np.std(final_values, ddof=1)  # Sample standard deviation
    skewness = stats.skew(final_values)
    kurt = stats.kurtosis(final_values)

    return {
        'mean': mean,
        'std': std,
        'skew': skewness,
        'kurtosis': kurt,
        'final_values': final_values
    }


def print_summary_statistics(summary_stats):
    """
    Print summary statistics in a readable format.

    Args:
        summary_stats (dict): Dictionary from calculate_summary_statistics
    """
    print("\n" + "="*60)
    print("SUMMARY STATISTICS OF FINAL DIFFERENCES")
    print("(Leveraged - Base stock value after 100 ticks)")
    print("="*60)
    print(f"Mean:              {summary_stats['mean']:>12.2f}")
    print(f"Standard Deviation:{summary_stats['std']:>12.2f}")
    print(f"Skewness:          {summary_stats['skew']:>12.2f}")
    print(f"Kurtosis:          {summary_stats['kurtosis']:>12.2f}")
    print("="*60)


def plot_histogram(final_values, filename="outcome_histogram.png"):
    """
    Plot a histogram of final outcome differences.

    Args:
        final_values (list): List of final difference values
        filename (str): Output filename for the histogram
    """
    plt.figure(figsize=(12, 8))

    # Create histogram
    n, bins, patches = plt.hist(final_values, bins=30, edgecolor='black', alpha=0.7)

    # Add vertical line for mean
    mean_val = np.mean(final_values)
    plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')

    # Add vertical line at 0
    plt.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5, label='Zero difference')

    plt.xlabel('Final Difference (Leveraged - Base)')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Final Outcomes\n({len(final_values)} simulations, {NUM_TICKS} ticks each)')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')

    # Save the plot
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Histogram saved to {filename}")

    # Display the plot
    plt.show()


def run_multi_graph():
    """
    Run multiple simulations and create graphs of trajectories and outcomes.
    """
    print(f"Running {500} simulations...")
    trajectories = run_multiple_simulations(num_runs=500, verbose=True)

    print(f"\nCompleted all simulations.")

    # Calculate and print summary statistics
    summary_stats = calculate_summary_statistics(trajectories)
    print_summary_statistics(summary_stats)

    # Create trajectory graph
    print("\nCreating trajectory graph...")
    plot_difference_trajectories(trajectories)

    # Create histogram
    print("Creating histogram...")
    plot_histogram(summary_stats['final_values'])

    print("\nAll visualizations complete!")


if __name__ == "__main__":
    # Run multiple simulations and graph them (default behavior)
    run_multi_graph()

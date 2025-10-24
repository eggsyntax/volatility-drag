# Leveraged Stock ETF Simulator

A Python application that simulates and visualizes the performance of a leveraged stock ETF compared to its underlying base stock, demonstrating the concept of **volatility drag**.

## What is Volatility Drag?

Volatility drag is a counterintuitive phenomenon where leveraged ETFs can underperform their expected returns over time, even when the underlying asset has positive expected returns. This happens because leveraged ETFs reset their leverage daily, and the compounding effect of volatility works against the investor.

This simulator helps build intuition for this effect by running hundreds of simulations and visualizing the outcomes.

## How It Works

The simulator models:
- A **base stock** starting at $1000 with daily returns following a normal distribution (mean: 0.02%, standard deviation: 6.0%)
- A **2x leveraged version** that gains or loses twice the percentage of the base stock each day
- Both stocks maintain running values over 100 daily ticks

After each simulation run, we track the difference between the leveraged stock value and the base stock value to see whether leverage helped or hurt.

## Installation

Requires Python 3.6+ with the following packages:

```bash
pip install numpy scipy matplotlib
```

## Usage

### Run Multiple Simulations (Default)

```bash
python stock_tracker.py
```

This will:
1. Run 500 simulations (100 ticks each)
2. Print summary statistics (mean, standard deviation, skewness, kurtosis)
3. Generate two graphs:
   - `multiple_runs.png` - Trajectory plot showing all 500 runs
   - `outcome_histogram.png` - Distribution of final outcomes

### Run a Single Simulation

To see detailed tick-by-tick output for a single run:

```python
from stock_tracker import main
main()
```

### Run Tests

```bash
python test_stock_tracker.py
```

## Configuration

You can modify these constants at the top of `stock_tracker.py`:

```python
MEAN_DAILY_CHANGE = 0.0002  # 0.02% average daily return
STDEV_DAILY_CHANGE = 0.06   # 6.0% daily volatility
INITIAL_VALUE = 1000.0      # Starting value for both stocks
NUM_TICKS = 100             # Number of days to simulate
```

You can also adjust:
- **Number of runs**: Change `num_runs` parameter in `run_multi_graph()` (default: 500)
- **Leverage ratio**: Modify `leveraged_change = daily_change * 2` to use different leverage (e.g., `* 3` for 3x leverage)

## Output

### Summary Statistics

The application prints statistics for the final difference (Leveraged - Base) across all runs:

```
============================================================
SUMMARY STATISTICS OF FINAL DIFFERENCES
(Leveraged - Base stock value after 100 ticks)
============================================================
Mean:                   -136.41
Standard Deviation:      784.06
Skewness:                  7.65
Kurtosis:                 64.81
============================================================
```

**Key insights:**
- **Negative mean**: On average, the leveraged version underperforms due to volatility drag
- **High standard deviation**: Massive variability in outcomes
- **Positive skewness**: Most outcomes cluster near zero or negative, but a few extreme positive outliers exist
- **High kurtosis**: Fat tails - extreme outcomes are much more common than a normal distribution would predict

### Visualizations

1. **Trajectory Plot (`multiple_runs.png`)**: Shows all 500 simulation runs as lines, with the x-axis representing tick number (0-100) and y-axis showing the difference between leveraged and base stock values. All lines start at 0.

2. **Histogram (`outcome_histogram.png`)**: Shows the distribution of final outcomes, with reference lines for the mean and zero difference.

## Files

- `stock_tracker.py` - Main application with simulation and visualization logic
- `test_stock_tracker.py` - Comprehensive test suite
- `run_multi_graph.py` - Convenience script (alternative way to run simulations)
- `multiple_runs.png` - Generated trajectory plot
- `outcome_histogram.png` - Generated histogram

## Example Findings

In a typical run with 500 simulations:
- Despite the base stock having a positive expected return (0.02% daily)
- The leveraged version underperforms on average by ~$136
- However, a small number of runs see spectacular gains (>$5000 difference)
- Most runs end up with modest losses or gains clustered around zero

This demonstrates why leveraged ETFs are generally not recommended for long-term holding, despite their appeal for short-term trading.

## License

This is educational software created to build intuition about volatility drag in leveraged instruments.

## Author

Created as a learning project to explore the mathematical properties of leveraged ETFs and volatility drag.

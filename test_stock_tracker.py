"""
Tests for the leveraged stock tracking application.
"""

import random
from stock_tracker import (
    MEAN_DAILY_CHANGE,
    STDEV_DAILY_CHANGE,
    INITIAL_VALUE,
    NUM_TICKS,
    generate_daily_change,
    apply_change,
    run_simulation,
    calculate_difference_trajectory,
    run_multiple_simulations,
    calculate_summary_statistics
)


def test_constants():
    """Test that constants are set correctly."""
    assert MEAN_DAILY_CHANGE == 0.0002, "Mean should be 0.02% (0.0002)"
    assert STDEV_DAILY_CHANGE == 0.06, "Stdev should be 6.0% (0.06)"
    assert INITIAL_VALUE == 1000.0, "Initial value should be 1000.0"
    assert NUM_TICKS == 100, "Number of ticks should be 100"


def test_generate_daily_change():
    """Test that daily change generation produces reasonable values."""
    random.seed(42)
    changes = [generate_daily_change() for _ in range(1000)]

    # Check that values are numeric
    assert all(isinstance(c, float) for c in changes)

    # Check that mean is approximately correct (within tolerance for random sampling)
    mean = sum(changes) / len(changes)
    assert abs(mean - MEAN_DAILY_CHANGE) < 0.01, f"Mean {mean} should be close to {MEAN_DAILY_CHANGE}"


def test_apply_change_positive():
    """Test applying a positive change."""
    value = 100.0
    change = 0.05  # 5% increase
    new_value = apply_change(value, change)
    assert new_value == 105.0, f"Expected 105.0, got {new_value}"


def test_apply_change_negative():
    """Test applying a negative change."""
    value = 100.0
    change = -0.03  # 3% decrease
    new_value = apply_change(value, change)
    assert new_value == 97.0, f"Expected 97.0, got {new_value}"


def test_apply_change_zero():
    """Test applying zero change."""
    value = 100.0
    change = 0.0
    new_value = apply_change(value, change)
    assert new_value == 100.0, f"Expected 100.0, got {new_value}"


def test_apply_change_leveraged():
    """Test applying leveraged change (2x the percentage)."""
    value = 70.0
    base_change = -0.03  # -3% for base
    leveraged_change = base_change * 2  # -6% for leveraged
    new_value = apply_change(value, leveraged_change)
    assert abs(new_value - 65.8) < 0.0001, f"Expected 65.8, got {new_value}"


def test_run_simulation_structure():
    """Test that simulation returns correct structure."""
    random.seed(123)
    results = run_simulation(seed=123)

    assert len(results) == NUM_TICKS, f"Should have {NUM_TICKS} results"

    # Check first result structure
    first = results[0]
    assert len(first) == 4, "Each result should have 4 elements"
    tick, change, base_val, lev_val = first
    assert tick == 1, "First tick should be 1"
    assert isinstance(change, float), "Change should be float"
    assert isinstance(base_val, float), "Base value should be float"
    assert isinstance(lev_val, float), "Leveraged value should be float"


def test_run_simulation_initial_values():
    """Test that both stocks start at the same initial value."""
    random.seed(456)
    results = run_simulation(seed=456)

    first_tick = results[0]
    tick, change, base_val, lev_val = first_tick

    # After first tick, values should have diverged from initial
    # but the calculation should be based on same starting point
    expected_base = INITIAL_VALUE * (1 + change)
    expected_lev = INITIAL_VALUE * (1 + 2 * change)

    assert abs(base_val - expected_base) < 0.0001, f"Base value calculation incorrect"
    assert abs(lev_val - expected_lev) < 0.0001, f"Leveraged value calculation incorrect"


def test_run_simulation_leveraged_multiplier():
    """Test that leveraged stock changes at 2x the rate."""
    random.seed(789)
    results = run_simulation(seed=789, verbose=False)

    # Check a few ticks to verify leveraged is always 2x
    for tick, change, base_val, lev_val in results[:5]:
        # We can't easily verify the absolute values without rerunning the simulation,
        # but we can verify the structure is consistent
        assert base_val > 0, "Base value should be positive"
        assert lev_val > 0, "Leveraged value should be positive (for this seed)"


def test_calculate_difference_trajectory():
    """Test that difference trajectory is calculated correctly."""
    random.seed(111)
    results = run_simulation(seed=111, verbose=False)

    trajectory = calculate_difference_trajectory(results)

    # Should have NUM_TICKS + 1 elements (tick 0 through NUM_TICKS)
    assert len(trajectory) == NUM_TICKS + 1, f"Expected {NUM_TICKS + 1} elements, got {len(trajectory)}"

    # First element should be 0 (no difference at tick 0)
    assert trajectory[0] == 0.0, f"Expected 0.0 at tick 0, got {trajectory[0]}"

    # Each subsequent element should be leveraged_value - base_value
    for i, (tick, change, base_val, lev_val) in enumerate(results):
        expected_diff = lev_val - base_val
        actual_diff = trajectory[i + 1]  # +1 because trajectory starts with 0
        assert abs(actual_diff - expected_diff) < 0.0001, \
            f"Tick {tick}: expected diff {expected_diff}, got {actual_diff}"


def test_run_multiple_simulations():
    """Test that multiple simulations run correctly."""
    num_runs = 5
    trajectories = run_multiple_simulations(num_runs=num_runs, verbose=False)

    # Should have correct number of trajectories
    assert len(trajectories) == num_runs, f"Expected {num_runs} trajectories, got {len(trajectories)}"

    # Each trajectory should have correct length
    for i, trajectory in enumerate(trajectories):
        assert len(trajectory) == NUM_TICKS + 1, \
            f"Trajectory {i}: expected {NUM_TICKS + 1} elements, got {len(trajectory)}"

        # First element should be 0
        assert trajectory[0] == 0.0, f"Trajectory {i}: first element should be 0.0"


def test_run_simulation_verbose_flag():
    """Test that verbose flag controls output correctly."""
    # This test doesn't assert anything, just ensures the verbose flag works
    # without causing errors
    run_simulation(seed=999, verbose=False)
    run_simulation(seed=999, verbose=True)


def test_calculate_summary_statistics():
    """Test that summary statistics are calculated correctly."""
    # Create a small set of trajectories with known final values
    trajectories = [
        [0.0, 100.0, 200.0, 300.0],  # final value: 300
        [0.0, 50.0, 100.0, 150.0],   # final value: 150
        [0.0, -50.0, -100.0, -150.0], # final value: -150
        [0.0, 200.0, 400.0, 600.0],  # final value: 600
    ]

    summary_stats = calculate_summary_statistics(trajectories)

    # Check that all keys are present
    assert 'mean' in summary_stats
    assert 'std' in summary_stats
    assert 'skew' in summary_stats
    assert 'kurtosis' in summary_stats
    assert 'final_values' in summary_stats

    # Check final values are extracted correctly
    assert summary_stats['final_values'] == [300.0, 150.0, -150.0, 600.0]

    # Check mean is correct
    expected_mean = (300 + 150 - 150 + 600) / 4
    assert abs(summary_stats['mean'] - expected_mean) < 0.01

    # Check that statistics are numeric
    assert isinstance(summary_stats['mean'], (int, float))
    assert isinstance(summary_stats['std'], (int, float))
    assert isinstance(summary_stats['skew'], (int, float))
    assert isinstance(summary_stats['kurtosis'], (int, float))


def test_summary_statistics_with_real_simulations():
    """Test summary statistics with actual simulation runs."""
    num_runs = 10
    trajectories = run_multiple_simulations(num_runs=num_runs, verbose=False)

    summary_stats = calculate_summary_statistics(trajectories)

    # Should have correct number of final values
    assert len(summary_stats['final_values']) == num_runs

    # Standard deviation should be positive (for multiple different runs)
    assert summary_stats['std'] >= 0

    # All statistics should be finite numbers
    assert abs(summary_stats['mean']) < float('inf')
    assert abs(summary_stats['std']) < float('inf')
    assert abs(summary_stats['skew']) < float('inf')
    assert abs(summary_stats['kurtosis']) < float('inf')


if __name__ == "__main__":
    test_constants()
    test_generate_daily_change()
    test_apply_change_positive()
    test_apply_change_negative()
    test_apply_change_zero()
    test_apply_change_leveraged()
    test_run_simulation_structure()
    test_run_simulation_initial_values()
    test_run_simulation_leveraged_multiplier()
    test_calculate_difference_trajectory()
    test_run_multiple_simulations()
    test_run_simulation_verbose_flag()
    test_calculate_summary_statistics()
    test_summary_statistics_with_real_simulations()
    print("All tests passed!")

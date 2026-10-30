import numpy as np
import pandas as pd


def create_random_series(n=10, seed=42):
    """Return a Series of n reproducible random integers from 1 to 99."""
    rng = np.random.default_rng(seed)
    values = rng.integers(low=1, high=100, size=n)
    return pd.Series(values)


def create_labeled_series(series):
    """Attach custom labels to an existing Series."""
    labels = [f"num_{i + 1}" for i in range(len(series))]
    return pd.Series(series.values, index=labels)


def describe_series(s, title="Series"):
    """Print a Series and its basic attributes."""
    print(f"{title}:")
    print(s)
    print(f"\nDtype : {s.dtype}")
    print(f"Shape : {s.shape}")
    print(f"Size  : {s.size}")
    print(f"Index : {list(s.index)}")


if __name__ == "__main__":
    # Step 1: create a Series with the default index
    series = create_random_series()
    print("STEP 1: Series with the default index")
    describe_series(series)

    # Step 2: create the same values with custom labels
    labeled = create_labeled_series(series)
    print("\nSTEP 2: Same values, custom labels")
    describe_series(labeled, title="Labeled Series")

    # Step 3: basic statistics
    print("\nSTEP 3: Basic statistics")
    print(f"Minimum : {series.min()}")
    print(f"Maximum : {series.max()}")
    print(f"Mean    : {series.mean():.2f}")
    print(f"Sum     : {series.sum()}")

    # Step 4: sorting
    print("\nSTEP 4: Sorted values (ascending)")
    print(series.sort_values().to_string())

    # Step 5: indexing and filtering
    print("\nSTEP 5: Indexing and filtering")
    print(f"First value (series.iloc[0]) : {series.iloc[0]}")
    print("Values greater than 50:")
    print(series[series > 50].to_string())

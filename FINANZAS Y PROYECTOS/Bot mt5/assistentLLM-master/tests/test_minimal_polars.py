import polars as pl
import numpy as np
import numba as nb

@nb.njit
def test_numba(arr):
    return arr * 2

def test_minimal():
    try:
        print("Testing Polars...")
        df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        print(f"Polars DataFrame created. Shape: {df.shape}")
        
        print("Testing Numba...")
        arr = np.array([1.0, 2.0, 3.0])
        res = test_numba(arr)
        print(f"Numba result: {res}")
        
        print("Minimal test finished successfully.")
    except Exception as e:
        print(f"Error during minimal test: {e}")

if __name__ == "__main__":
    test_minimal()

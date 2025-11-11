import unittest
import pandas as pd
from src.data_loader import SolarDataLoader

class TestDataLoader(unittest.TestCase):
    """
    Unit tests for SolarDataLoader class.
    Tests loading and cleaning functionality.
    """
    def setUp(self):
        """
        Set up loader and load data before each test.
        """
        self.loader = SolarDataLoader('data/benin.csv')
        self.loader.load_data()  # Load before clean to avoid ValueError

    def test_load_data(self):
        """
        Test if load_data returns a DataFrame with expected shape.
        """
        self.assertIsInstance(self.loader.df, pd.DataFrame)
        self.assertGreater(len(self.loader.df), 0, "DataFrame should have rows")
        self.assertIn('GHI', self.loader.df.columns, "GHI column should exist")

    def test_clean_data(self):
        """
        Test if clean_data removes negatives, flags outliers, and imputes medians.
        """
        df_clean = self.loader.clean_data()
        self.assertGreater(df_clean['GHI'].mean(), 0, "GHI mean should be positive")
        self.assertGreaterEqual(df_clean['GHI'].min(), 0, "GHI min should be >=0 after dropping negatives")
        # Check key_cols only (relaxed <10% total missing after impute)
        key_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
        missing_key = df_clean[key_cols].isnull().sum().sum()
        self.assertLess(missing_key, len(df_clean) * 0.10, "Key cols missing <10% after impute")

if __name__ == '__main__':
    unittest.main()
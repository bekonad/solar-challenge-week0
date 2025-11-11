import unittest
import pandas as pd
from src.data_loader import SolarDataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = SolarDataLoader('data/benin.csv')
        self.loader.load_data()  # Load before clean

    def test_load_data(self):
        self.assertIsInstance(self.loader.df, pd.DataFrame)
        self.assertGreater(len(self.loader.df), 0)

    def test_clean_data(self):
        df_clean = self.loader.clean_data()
        self.assertGreater(df_clean['GHI'].mean(), 0)
        self.assertGreater(df_clean['GHI'].min(), -1)  # No negatives

if __name__ == '__main__':
    unittest.main()
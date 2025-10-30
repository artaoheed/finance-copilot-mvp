import pandas as pd

def test_csv_parser():
    df = pd.read_csv("data/sample_transactions.csv")
    assert not df.empty, "CSV file should not be empty"
    assert "amount" in df.columns, "Amount column missing"
    assert df["amount"].dtype in [float, int], "Amount column must be numeric"

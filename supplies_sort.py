"""
Import supplies.csv into pandas dataframe and pivot on ItemNumber Column
"""

import pandas as pd

if __name__ == "__main__":

    with open("./download/supplies.csv", "r") as file:
        supplies = pd.read_csv(file)

    supplies = supplies.pivot_table(
        index=[
            "ItemNumber",
            "ItemDescription",
            "CasePackQuantity",
            "ManufacturerName",
            "UOM",
        ],
        values="QuantityShipped",
        aggfunc="sum",
    )

    print(supplies.describe())

    supplies.to_csv("./download/supply_items.csv")

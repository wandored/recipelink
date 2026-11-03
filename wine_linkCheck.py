import csv
import os
import re
import pandas as pd
from icecream import ic


merge1 = pd.DataFrame()


def remove_vendors(df, rest):
    """
    Remove vendors that are not used by the restaurant
    """
    file = open("./linkcheck/" + rest + "_vendors.txt")
    vendor_list = file.read().split("\n")
    file.close
    df = df[df["Vendor"].isin(vendor_list)]
    return df


def extract_bin_numbers(row, regex):
    for col in row.index:
        if isinstance(row[col], str) and re.match(regex, row[col]):
            ic(row[col])
            return row[col]
    return None


def main():
    store_list = ["atlanta", "boca", "ch47", "chno", "myrtle"]
    os.system("clear")

    for store in store_list:
        menuitems = pd.read_csv(
            "./linkcheck/wine_menu_items.csv",
            sep=",",
            usecols=["Name", "Recipe"],
            dtype=str,
        )
        bin_numbers = pd.read_csv(
            "../pos_data_exports/output/wine_bin_numbers.csv", sep=",", dtype=str
        )
        ingredients = pd.read_csv(
            "./linkcheck/wine_ingredients.csv", sep=",", usecols=["Item", "Recipe"]
        )
        stockCount = pd.read_csv(
            "./linkcheck/" + store + "_stock_count.csv", sep=",", usecols=["Item"]
        )
        vendorItems = pd.read_csv(
            "./linkcheck/wine_vendor_items.csv",
            sep=",",
            usecols=["Item", "Vendor", "PurchasingUofM", "VendorItemNumber"],
        )

        # vendorItems = remove_vendors(vendorItems, store)

        menuitems["Name"] = menuitems["Name"].str.replace("Steakhouse - ", "")
        menuitems.rename(columns={"Name": "Toast"}, inplace=True)
        ingredients.rename(columns={"Item": "Purchase Item"}, inplace=True)
        stockCount.rename(columns={"Item": "Purchase Item"}, inplace=True)
        vendorItems.rename(columns={"Item": "Purchase Item"}, inplace=True)

        merge0 = pd.merge(menuitems, bin_numbers, on="Toast", how="left")
        merge1 = pd.merge(merge0, ingredients, on="Recipe", how="left")
        merge1["ATL"] = merge1.apply(
            extract_bin_numbers, axis=1, args=(r"[A]\d{3,4}$",)
        )
        merge1["BOCA"] = merge1.apply(
            extract_bin_numbers, axis=1, args=(r"[B]\d{3,4}$",)
        )
        merge1["MB"] = merge1.apply(extract_bin_numbers, axis=1, args=(r"[M]\d{3,4}$",))
        merge1["CH47"] = merge1.apply(
            extract_bin_numbers, axis=1, args=(r"[G]\d{3,4}$",)
        )
        merge1["NOLA"] = merge1.apply(
            extract_bin_numbers, axis=1, args=(r"[L]\d{3,4}$",)
        )
        merge1.drop(columns=["Bin0", "Bin1", "Bin2", "Bin3", "Bin4"], inplace=True)
        col_order = [
            "Toast",
            "ATL",
            "BOCA",
            "MB",
            "CH47",
            "NOLA",
            "Recipe",
            "Purchase Item",
        ]
        merge1 = merge1[col_order]

        in_toast = pd.merge(merge1, stockCount, on="Purchase Item", how="left")
        in_stockcount = pd.merge(merge1, stockCount, on="Purchase Item", how="right")
        in_both = pd.merge(merge1, stockCount, on="Purchase Item", how="inner")

        in_toast.sort_values(by="Purchase Item", inplace=True)
        in_toast.drop(columns=["Recipe"], inplace=True)
        in_toast = in_toast[in_toast["Purchase Item"].isna()]

        in_stockcount.sort_values(by="Purchase Item", inplace=True)
        in_stockcount.drop(columns=["Recipe"], inplace=True)
        in_stockcount = in_stockcount[in_stockcount["Toast"].isna()]

        in_both.sort_values(by="Purchase Item", inplace=True)
        in_both.drop(columns=["Recipe"], inplace=True)

        # linkCheck = pd.merge(merge2, vendorItems, on='Purchase Item', how='left')
        #        linkCheck.dropna(subset=['Toast'], thresh=1, inplace=True)

        with pd.ExcelWriter(f"./output/{store}_WineCheck.xlsx") as writer:  # pylint: disable=abstract-class-instantiated
            in_toast.to_excel(writer, sheet_name="In Toast")
            in_stockcount.to_excel(writer, sheet_name="In StockCount")
            in_both.to_excel(writer, sheet_name="In Both")

    ic(merge1)

    with pd.ExcelWriter("./output/WineCheck.xlsx") as writer:  # pylint: disable=abstract-class-instantiated
        merge1.sort_values(by="Toast", inplace=True)
        merge1.to_excel(writer)


if __name__ == "__main__":
    main()
#    os.system("cp /home/wandored/Projects/r365cleaner/output/*_WineCheck.xlsx /home/wandored/Dropbox/Restaurant365/Report_Data")

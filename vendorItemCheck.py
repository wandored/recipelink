"""
read csv files into pandas dataframe
merge dataframes to find conflicts in vendor items
"""

import pandas as pd
from icecream import ic


def read_sysco():
    """
    read csv file into pandas dataframe
    """
    df = pd.read_csv(
            './download/sysco.csv',
            sep=',',
            usecols=['DC Name', 'Pack / Size', 'Product #', 'Product Desc'],
            dtype={'DC Name': str, 'Pack / Size': str, 'Product #': str, 'Product Desc': str}
            )
    df = df.rename(columns={'DC Name': 'Vendor', 'Pack / Size': 'PackSize', 'Product #': 'VendorItemNumber'})
    return df

def read_r365():
    """
    read csv file into pandas dataframe
    """
    df = pd.read_csv(
            './download/r365.csv',
            sep=',',
            usecols=['Item', 'Vendor', 'PurchasingUofM', 'SplitUofM', 'VendorItemNumber'],
            dtype={'Item': str, 'Vendor': str, 'PurchasingUofM': str, 'SplitUofM': str, 'VendorItemNumber': str}
            )
    df = df.rename(columns={'PurchasingUofM': 'UofM'})
    df['Vendor'] = df['Vendor'].str.replace('SYSCO', '')
    df['Vendor'] = df['Vendor'].str.replace('LLC', '')
    df['Vendor'] = df['Vendor'].str.replace(', INC', '')
    df['Vendor'] = df['Vendor'].str.replace('FOOD SERVICES OF FL', 'SOUTHEAST FLORIDA')
    df['Vendor'] = df['Vendor'].str.strip()
    return df



if __name__ == '__main__':
    # read csv files into pandas dataframes
    df1 = read_sysco()
    df2 = read_r365()
    # merge dataframes to find conflicts in vendor items
    df3 = pd.merge(df1, df2, how='right', on=['Vendor', 'VendorItemNumber'])
    df3 = df3.sort_values(by='VendorItemNumber')
    # reorder columns
    df3 = df3[['Item', 'Vendor', 'VendorItemNumber', 'Product Desc', 'PackSize', 'UofM', 'SplitUofM']]
    ic(df3.head(50))
    # write to xlsx file
    df3.to_excel('./output/vendorItemCheck.xlsx', index=False)

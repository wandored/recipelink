import csv
import os
import pandas as pd
from icecream import ic


def remove_vendors(df, rest):
    # Removes unused vendors from the dataframes
    file = open('./linkcheck/'+rest+'_vendors.txt')
    vendor_list = file.read().split('\n')
    file.close
    df = df[df['Vendor'].isin(vendor_list)]
    return df


def main():

    store_list = ['atlanta', 'boca', 'ch47', 'chno', 'myrtle']

    os.system('clear')

    for store in store_list:
        menuitems = pd.read_csv('./linkcheck/wine_menu_items.csv', sep=',', usecols=['Name', 'Recipe'])
        ingredients = pd.read_csv('./linkcheck/wine_ingredients.csv', sep=',', usecols=['Item', 'Recipe'])
        stockCount = pd.read_csv('./linkcheck/'+store+'_stock_count.csv', sep=',', usecols=['Item'])
        vendorItems = pd.read_csv('./linkcheck/wine_vendor_items.csv', sep=',', usecols=['Item', 'Vendor', 'PurchasingUofM', 'VendorItemNumber'])

        #vendorItems = remove_vendors(vendorItems, store)

        menuitems['Name'] = menuitems['Name'].str.replace('Steakhouse - ', '')
        menuitems.rename(columns={'Name': 'Toast'}, inplace=True)

        ingredients.rename(columns={'Item': 'Purchase Item'}, inplace=True)
        stockCount.rename(columns={'Item': 'Purchase Item'}, inplace=True)
        vendorItems.rename(columns={'Item': 'Purchase Item'}, inplace=True)

        merge1 = pd.merge(menuitems, ingredients, on='Recipe', how='left')
        merge1.drop(columns=['Recipe'], inplace=True)
        merge2 = pd.merge(merge1, stockCount, on='Purchase Item', how='outer')

        linkCheck = pd.merge(merge2, vendorItems, on='Purchase Item', how='left')
#        linkCheck.dropna(subset=['Toast'], thresh=1, inplace=True)

        with pd.ExcelWriter(f'./output/{store}_WineCheck.xlsx') as writer:     # pylint: disable=abstract-class-instantiated
            linkCheck.sort_values(by='Purchase Item', inplace=True)
            linkCheck.to_excel(writer)
        print(linkCheck.info())


if __name__ == '__main__':
    main()
#    os.system("cp /home/wandored/Projects/r365cleaner/output/*_WineCheck.xlsx /home/wandored/Dropbox/Restaurant365/Report_Data")

import csv
import os
import pandas as pd


def remove_vendors(df, rest):
    # Removes unused vendors from the dataframes
    file = open('./linkcheck/'+rest+'_vendors.txt')
    vendor_list = file.read().split('\n')
    file.close
    df = df[df['Vendor'].isin(vendor_list)]
    return df


store_list = ['Atlanta', 'Boca', 'CH47', 'CHNO', 'Myrtle']

for store in store_list:
    os.system('sed -i "s/CAFÉ/CAFE/g" ./linkcheck/'+store+'_menu_items.csv')
    os.system('sed -i "s/\ -\ /-/g2" ./linkcheck/'+store+'_menu_items.csv')
    os.system('sed -i "s/CHOPHOUSE\ -\ NOLA/CHOPHOUSE-NOLA/g" ./linkcheck/' +
              store+'_menu_items.csv')
os.system(
    'sed -i "s/CHOPHOUSE\ -\ NOLA/CHOPHOUSE-NOLA/g" ./linkcheck/wine_ingredients.csv')
os.system(
    'sed -i "s/CHOPHOUSE\ -\ NOLA/CHOPHOUSE-NOLA/g" ./linkcheck/wine_vendor_items.csv')
os.system('sed -i "s/\ -\ /-/g2" ./linkcheck/wine_ingredients.csv')
os.system('sed -i "s/\ -\ /-/g2" ./linkcheck/wine_vendor_items.csv')
os.system('sed -i "s/CAFÉ/CAFE/g" ./linkcheck/wine_ingredients.csv')
os.system('sed -i "s/CAFÉ/CAFE/g" ./linkcheck/wine_vendor_items.csv')

os.system('clear')

for store in store_list:
    df_menuItems = pd.read_csv('./linkcheck/'+store+'_menu_items.csv', sep=',')
    df_ingredients = pd.read_csv('./linkcheck/wine_ingredients.csv', sep=',')
    df_stockCount = pd.read_csv(
        './linkcheck/'+store+'_Stock_Count.csv', sep=',')
    df_vendorItems = pd.read_csv('./linkcheck/wine_vendor_items.csv', sep=',')
    df_vendorItems = remove_vendors(df_vendorItems, store)

    df_menuItems.drop(
        columns={'RecipeId', 'MenuItemId', '__count'}, inplace=True)
    df_menuItems.rename(columns={'Name': 'POSI'}, inplace=True)

    df_ingredients.drop(
        columns={'Qty', 'UofM', 'IngredientId', '__count'}, inplace=True)
    df_ingredients.rename(columns={'Item': 'Purchase Item'}, inplace=True)

    df_stockCount.drop(columns={'SLSort', 'UofM', 'Qty',
                       'UofM2', 'Qty2', 'UofM3', 'Qty3'}, inplace=True)
    df_stockCount.rename(columns={'Item': 'Purchase Item'}, inplace=True)

    df_vendorItems.drop(
        columns={'Name', 'VendorItemId', '__count'}, inplace=True)
    df_vendorItems.rename(columns={'Item': 'Purchase Item'}, inplace=True)

    df_merge1 = pd.merge(df_menuItems, df_ingredients,
                         on='Recipe', how='outer')
    df_merge2 = pd.merge(df_merge1, df_stockCount,
                         on='Purchase Item', how='outer')
    df_linkCheck = pd.merge(df_merge2, df_vendorItems,
                            on='Purchase Item', how='outer')

    df_linkCheck.dropna(
        subset=['POSI', 'StorageLocation'], thresh=1, inplace=True)

    with pd.ExcelWriter(f'./output/{store}_WineCheck.xlsx') as writer:     # pylint: disable=abstract-class-instantiated
        df_linkCheck.sort_values(by='StorageLocation', inplace=True)
        df_linkCheck.to_excel(writer)
    print(df_linkCheck.info())

# os.system("cp /home/wandored/Projects/r365cleaner/output/*_WineCheck.xlsx /home/wandored/Dropbox/Restaurant365/Report_Data")

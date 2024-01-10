# Wine Check Tool

## Overview

This Python script is a tool for performing a wine inventory check for multiple restaurant locations. It reads data from various CSV files, processes and merges the data, and outputs the result in Excel format. The tool is designed to be used with specific data files and follows a specific workflow to generate a consolidated wine check report for each restaurant location.

## Prerequisites

- Python 3.x
- pandas library (`pip install pandas`)
- icecream library (`pip install icecream`)

## Usage

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/wine-check-tool.git
   cd wine-check-tool
   ```

2. Prepare the necessary input data:

   - Ensure that the required CSV files (`wine_menu_items.csv`, `wine_ingredients.csv`, `wine_vendor_items.csv`, and `<store>_stock_count.csv`) are present in the `./linkcheck/` directory.

   - Create a `<store>_vendors.txt` file for each store in the `./linkcheck/` directory, containing a list of vendors to be included in the analysis.

3. Run the script:

   ```bash
   python wine_check_tool.py
   ```

4. Review the generated Excel files:

   The script will create Excel files in the `./output/` directory, named `<store>_WineCheck.xlsx` for each store. These files contain the consolidated wine check report.

## Configuration

- Modify the `store_list` variable in the script to include the desired store locations.

## Output

The script generates an Excel file for each store, containing a consolidated wine check report. The report includes information about menu items, recipes, ingredients, stock count, and vendor items.

## Notes

- The script uses the `icecream` library for debugging purposes. Remove or comment out the `ic` statements if not needed.

- The script may be customized further based on specific requirements or data structures.

## License

This script is released under the MIT License. See the [LICENSE](LICENSE) file for details.

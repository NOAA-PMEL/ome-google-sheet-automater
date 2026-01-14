import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Share sheets with python-api@zalmanek-brynn.iam.gserviceaccount.com

# Set up credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(
    'credentials.json', scopes=scopes)
client = gspread.authorize(creds)

# List of google sheets to combine, use the spreadsheet url format: (sheet_id, sheet_name)
spreadsheets_to_combine = [('16Zg1MbMupnkXzuypTg4aF37OMyytPd-ZRqfz9QNX2oI', 'Sheet1'),
                           ('1aXN_HmGRDgDLvkz1Dbkje6R7rUUg9mNNc630YN8HvFE', 'Sheet1'),
                           ('1r94A1MB5Gih0djnwEdxB15gv_h16EQ1qkUWZ8VUlW3I', 'Sheet1'),
                           ('1HPXc9LFixqyo-pDRfcn71N7OO-OJtWUdIbBdo62cnjA', 'Sheet1'),
                           ('1KTs7LiITWi4DxmAjevH19HkWzKDY4CSkmd184dKmKxQ',
                            'Extraction Sheets'),
                           ('1K4XrXplTNukaeIY_UQ_XXuYLBuvJwJmaeEbAZvHSiEI',
                            'Extraction Sheet'),
                           ('1Wqg7Xjqhh1c5u1S6eTsY45fxzFOBxASF2oPkMno4580',
                            'Extraction Sheet'),
                           ('1_Oa4CievaRjUFxI7xceAA3NIS6IlUdobtA0_Ahi1arI',
                            'Extraction Sheet'),
                           ('1I5WKkoXY_TBQbVDe16KSAAZxG5vKptbQW9MArA8WtWA',
                            'Extraction Sheet'),
                           ('1LftDxnIXT6rsPExrotJDRuGyzyxo77kl_OBlsbZDe6c',
                            'Extraction Sheet'),
                           ('15Y9PHErqbco65sbAZzqWI75PH9dqsSZNhvPdO-tHFJY', 'Extraction Sheet')]

# Name of destination spreadsheet and sheet name
destination_spreadsheet_id = '1x8Fe44qQRQE1RlXnDkj6Kx0aN9Ra0--eaHH09P_zhwo'
destination_sheet_name = 'Sheet1'

dfs = []
for spreadsheet_id, sheet_name in spreadsheets_to_combine:
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        data = sheet.get_all_values()
        if len(data) > 1:
            # Create df and make columns unique
            df = pd.DataFrame(data[1:], columns=data[0])

            # Fix duplicate column names by adding suffixes
            cols = pd.Series(df.columns)
            for dup in cols[cols.duplicated()].unique():
                cols[cols == dup] = [
                    dup if i == 0 else f"{dup}.{i}" for i, col in enumerate(cols[cols == dup])]
            df.columns = cols
            dfs.append(df)
            print(
                f"✔ Loaded {len(df)} rows from {spreadsheet.title} - {sheet_name}")
        else:
            print(f"⚠️ No data in {spreadsheet.title} - {sheet_name}")
    except Exception as e:
        print(f"✘ Error loading {spreadsheet.title} ({spreadsheet_id}): {e}")

# Concatenate all data frames
combined_df = pd.concat(dfs, ignore_index=True, sort=False)
print(
    f"\n📊 Combined: {len(combined_df)} rows, {len(combined_df.columns)} columns")

# load destination sheet and clear
dest_spreadsheet = client.open_by_key(destination_spreadsheet_id)
combined_sheet = dest_spreadsheet.worksheet(destination_sheet_name)
combined_sheet.clear()

# Convert dataframe to list format (without index)
data_to_write = [combined_df.columns.values.tolist()] + \
    combined_df.fillna('').values.tolist()

# Write data
combined_sheet.update(values=data_to_write, range_name='A1')

# Freeze header and first column
combined_sheet.freeze(rows=1, cols=1)
print(f"✅ Done! {dest_spreadsheet.url}")

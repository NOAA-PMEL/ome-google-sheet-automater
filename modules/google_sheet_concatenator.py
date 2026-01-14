import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import yaml

# Share sheets with python-api@zalmanek-brynn.iam.gserviceaccount.com


class GoogleSheetConcatenator:

    def __init__(self, config_yaml: str, credentials: str):
        """
        config_yaml: path to yaml file with spreadsheets to combine (id and sheet name), destination sheet id and destination sheet name
        credentials: path to json file with google auth credentials
        """
        self.config_yaml = config_yaml
        self.creds = credentials
        self.client = self.setup_google_client()
        self.spreadsheets_to_combine, self.destination_sheet_id, self.destination_sheet_name = self.read_confg()
        self.write_data_to_master_sheet()

    def read_confg(self):
        with open(self.config_yaml, 'r') as f:
            data = yaml.safe_load(f)
            # Convert list of lists to list of tuples just to be safe
        spreadsheets_to_combine = [tuple(item)
                                   for item in data['sheets_to_combine']]
        destination_sheet_id = data['destination_spreadsheet_id']
        destination_sheet_name = data['destination_sheet_name']

        return (spreadsheets_to_combine, destination_sheet_id, destination_sheet_name)

    def setup_google_client(self):
        # Set up credentials
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(
            self.creds, scopes=scopes)
        client = gspread.authorize(creds)
        return client

    def combine_sheets_into_one_df(self) -> pd.DataFrame:
        """Combine all the sheets into one pandas data frame"""
        dfs = []
        for spreadsheet_id, sheet_name in self.spreadsheets_to_combine:
            try:
                spreadsheet = self.client.open_by_key(spreadsheet_id)
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
                print(
                    f"✘ Error loading {spreadsheet.title} ({spreadsheet_id}): {e}")

        # Concatenate all data frames
        combined_df = pd.concat(dfs, ignore_index=True, sort=False)
        print(
            f"\n📊 Combined: {len(combined_df)} rows, {len(combined_df.columns)} columns")

        return combined_df

    def write_data_to_master_sheet(self):
        """Write the combined sheet data to the master destination sheet"""
        combined_df = self.combine_sheets_into_one_df()

        # load destination sheet and clear
        dest_spreadsheet = self.client.open_by_key(self.destination_sheet_id)
        combined_sheet = dest_spreadsheet.worksheet(
            self.destination_sheet_name)
        combined_sheet.clear()

        # Convert dataframe to list format (without index)
        data_to_write = [combined_df.columns.values.tolist()] + \
            combined_df.fillna('').values.tolist()

        # Write data
        combined_sheet.update(values=data_to_write, range_name='A1')

        # Freeze header and first column
        combined_sheet.freeze(rows=1, cols=1)
        print(f"✅ Done! {dest_spreadsheet.url}")

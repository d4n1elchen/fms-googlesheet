# fms-googlesheet

かふかふ

## Usage

Place your Google Sheets service account in `service_account.json` and run the following command to update the sheet with the latest FMS data. See https://docs.gspread.org/en/latest/oauth2.html for more details on how to set up the service account.

```bash
python main.py --sheet_id YOUR_SHEET_ID
```

Or explicitly specify the path to your service account file:

```bash
python main.py --sheet_id YOUR_SHEET_ID --service_account path/to/service_account.json
```

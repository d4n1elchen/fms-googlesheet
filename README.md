# fms-googlesheet

Place your Google Sheets credentials in `credentials.json` and run the following command to update the sheet with the latest FMS data.

```bash
python main.py --sheet_id YOUR_SHEET_ID
```

Or explicitly specify the path to your credentials file:

```bash
python main.py --sheet_id YOUR_SHEET_ID --credentials path/to/credentials.json
```

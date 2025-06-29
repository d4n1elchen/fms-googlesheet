import argparse
import datetime
from typing import Any

import gspread
from fmslist import FindMeStoreItemList

parser = argparse.ArgumentParser(description="A simple example script.")
parser.add_argument(
    "--sheet_id", type=str, help="The id of the Google Sheet to update."
)
parser.add_argument(
    "--credentials",
    type=str,
    help="Path to the Google API credentials file.",
    default="credentials.json",
)
parser.add_argument(
    "--token",
    type=str,
    help="Path to save/read the Google API token file.",
    default="token.json",
)


def main():
    args = parser.parse_args()

    gc = gspread.oauth(
        credentials_filename=args.credentials, authorized_user_filename=args.token
    )

    fms = FindMeStoreItemList()

    wks = gc.open_by_key(args.sheet_id).sheet1
    wks.clear()

    # Update a range of cells using the top left corner address
    headers = [
        "ID",
        "Title",
        "Product Type",
        "Vendor",
        "Link",
        "Published At",
        "Variant",
        "Price",
        "Available",
        "Quantity",
        "Preorder Start",
        "Preorder End",
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ]
    rows: list[list[Any]] = [headers]
    rows.extend(
        [
            [
                variant.id,
                item.title,
                item.product_type,
                item.vendor,
                item.link,
                item.published_at.strftime("%Y-%m-%d %H:%M:%S"),
                variant.name if variant.name else "-",
                variant.price,
                variant.available,
                variant.quantity,
                (
                    item.preorder_period.start_time.strftime("%Y-%m-%d %H:%M")
                    if item.preorder_period
                    else None
                ),
                (
                    item.preorder_period.end_time.strftime("%Y-%m-%d %H:%M")
                    if item.preorder_period
                    else None
                ),
            ]
            for item in fms.get_items(fill_preorder_period=True)
            for variant in item.variants
        ]
    )
    wks.update(rows, "A1")
    wks.format("1:1", {"textFormat": {"bold": True}})


if __name__ == "__main__":
    main()

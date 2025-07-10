import argparse
import datetime
from typing import Any

import gspread
import pytz
from fmslist import FindMeStoreItemList

parser = argparse.ArgumentParser(description="A simple example script.")
parser.add_argument(
    "--sheet_id", type=str, help="The id of the Google Sheet to update."
)
parser.add_argument(
    "--service_account",
    type=str,
    help="Path to the Google API service_account file.",
    default="service_account.json",
)


def main():
    args = parser.parse_args()

    gc = gspread.service_account(filename=args.service_account)

    fms = FindMeStoreItemList()
    items = fms.get_items(fill_preorder_period=True)

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
        datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S%z"),
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
                item.published_at.strftime("%Y-%m-%d %H:%M:%S%z"),
                variant.name if variant.name else "-",
                variant.price,
                variant.available,
                variant.quantity,
                (
                    item.preorder_period.start_time.strftime("%Y-%m-%d %H:%M%z")
                    if item.preorder_period
                    else None
                ),
                (
                    item.preorder_period.end_time.strftime("%Y-%m-%d %H:%M%z")
                    if item.preorder_period
                    else None
                ),
            ]
            for item in items
            for variant in item.variants
        ]
    )
    wks.update(rows, "A1")
    wks.format("1:1", {"textFormat": {"bold": True}})


if __name__ == "__main__":
    main()

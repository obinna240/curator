import os
import csv
import json
import sys
import time
import requests
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")




contract_status = {
    "Open": 1,
    "Closed": 2,
    "Withdrawn": 4,
    "Awarded": 8,
    "Draft": 16,
}



def get_data(published_from, published_to):
    url = "https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json"
    criteria = {
        "searchCriteria": {
            "types": ["Contract"],
            "statuses": ["Awarded"],
            "publishedFrom": published_from.strftime("%Y-%m-%d"),
            "publishedTo": published_to.strftime("%Y-%m-%d"),
        },
        "size": 1000,
    }
    payload = json.dumps(criteria)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=payload, headers=headers, timeout=60)
    if response.status_code == 200:
        return response.json()
    if response.status_code == 403:
        print("Received 403 error. Waiting for 5 minutes before retrying...")
        time.sleep(300)
        return get_data(published_from, published_to)
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    print("Response content:")
    print(response.text)
    return None


def fetch_range(current_from, range_end):
    """Fetch a date range, narrowing the window if hitCount exceeds 1000."""
    for days in (30, 14, 7, 1):
        current_to = min(current_from + timedelta(days=days), range_end)
        print(
            f"Fetching data from {current_from.strftime('%Y-%m-%d')} to "
            f"{current_to.strftime('%Y-%m-%d')}"
        )
        data = get_data(current_from, current_to)
        if data is None:
            return None, current_to
        if data["hitCount"] <= 1000:
            return data, current_to
        print(
            f"More than 1000 results ({data['hitCount']}). "
            f"Adjusting range to {days}-day window."
        )
    current_to = current_from
    data = get_data(current_from, current_to)
    return data, current_to


def adjust_date_range(start_date, end_date, csv_file="data.csv"):
    field_names = [
        "id",
        "parentId",
        "noticeIdentifier",
        "title",
        "description",
        "cpvDescription",
        "cpvDescriptionExpanded",
        "publishedDate",
        "deadlineDate",
        "awardedDate",
        "awardedValue",
        "awardedSupplier",
        "approachMarketDate",
        "valueLow",
        "valueHigh",
        "postcode",
        "coordinates",
        "isSubNotice",
        "noticeType",
        "noticeStatus",
        "isSuitableForSme",
        "isSuitableForVco",
        "awardedToSme",
        "awardedToVcse",
        "lastNotifableUpdate",
        "organisationName",
        "sector",
        "cpvCodes",
        "cpvCodesExtended",
        "region",
        "regionText",
        "start",
        "end",
    ]

    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, csv_file)

    current_from = start_date
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names, extrasaction="ignore")
        writer.writeheader()

        while current_from <= end_date:
            data, current_to = fetch_range(current_from, end_date)

            if data and data["hitCount"] <= 1000:
                print(
                    f"Data fetched for range: {current_from.strftime('%Y-%m-%d')} to "
                    f"{current_to.strftime('%Y-%m-%d')}, Records: {data['hitCount']}"
                )
                for item in data["noticeList"]:
                    writer.writerow(item["item"])
            elif data and data["hitCount"] > 1000:
                print(
                    f"More than 1000 returns on: {current_from.strftime('%Y-%m-%d')} to "
                    f"{current_to.strftime('%Y-%m-%d')}, Records: {data['hitCount']}"
                )
                print("Cannot paginate further; date-range approach needs modifying.")
                sys.exit(1)
            else:
                print(
                    f"No data returned for range: {current_from.strftime('%Y-%m-%d')} to "
                    f"{current_to.strftime('%Y-%m-%d')}"
                )

            current_from = current_to + timedelta(days=1)

    print(f"Finished. Output written to {output_path}")


if __name__ == "__main__":
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2024, 5, 1)
    adjust_date_range(start_date, end_date)

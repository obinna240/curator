# Contracts Finder Scraper

`scraper.py` downloads awarded UK government contract notices from the [Contracts Finder](https://www.contractsfinder.service.gov.uk/) API and writes them to a CSV file.

## What it does

The script queries the Contracts Finder REST API for notices where:

- **Type:** Contract
- **Status:** Awarded

It walks forward in time from a start date to an end date, fetching results in batches. Each batch is written to `data/data.csv`.

The API returns at most 1,000 records per request. If a date range has more than 1,000 matches, the script automatically narrows the window (30 → 14 → 7 → 1 day) until the result set fits within the limit.

## Requirements

- Python 3.9+
- [requests](https://pypi.org/project/requests/)

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run with the default date range (2000-01-01 to 2024-05-01):

```bash
python scraper.py
```

Output is written to `data/data.csv`.

### Custom date range

Edit the dates at the bottom of `scraper.py`, or call `adjust_date_range` from another script:

```python
from datetime import datetime
from scraper import adjust_date_range

adjust_date_range(datetime(2024, 1, 1), datetime(2024, 12, 31))
```

You can also pass a custom output filename:

```python
adjust_date_range(datetime(2024, 1, 1), datetime(2024, 12, 31), csv_file="2024.csv")
```

## Output

The CSV includes fields such as:

| Field | Description |
|-------|-------------|
| `id` | Unique notice ID |
| `title` | Contract title |
| `description` | Full notice description |
| `publishedDate` | Date the notice was published |
| `awardedDate` | Date the contract was awarded |
| `awardedValue` | Contract value |
| `awardedSupplier` | Winning supplier |
| `organisationName` | Contracting authority |
| `region` / `regionText` | Geographic region |
| `cpvCodes` | Common Procurement Vocabulary codes |

See `field_names` in `adjust_date_range()` for the full list of columns.

## Behaviour notes

- **Rate limiting:** If the API returns HTTP 403, the script waits 5 minutes and retries the same request.
- **Long runs:** The default range spans over 24 years and will make many API calls. Start with a smaller date range to verify everything works.
- **Single-day overflow:** If a single day still returns more than 1,000 results, the script exits with an error. The date-range logic would need extending (e.g. intra-day timestamps) to handle that case.

## API reference

- Endpoint: `POST https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json`
- [Contracts Finder](https://www.contractsfinder.service.gov.uk/)

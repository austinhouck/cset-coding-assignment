# CSET Coding Assignment

This is a simple Python project that fulfills the requirements laid out in [TASK_INSTRUCTIONS.md](TASK_INSTRUCTIONS.md). It consists of a single script, `main.py`, and only uses four libraries:
- The built-in `csv` library, used for writing to CSV
- `beautifulsoup4`, a commonly-used web scraping library
- `requests`, to make HTTP requests
- `sys`, to read command-line arguments

## Install Requirements

This code requires Python 3.6+ to run. It is recommended to use Python 3.10+

```
pip install -r requirements.txt
```

## How to Run

To fetch data on all CSET staff, run the following command:

```
python -m main
```

By default, the script fetches data for all CSET staff members. To filter for data on specific teams, add the `--teams` flag to the command, followed by a comma-separated list of teams, like so:

```
python -m main --teams "Data Science,Emerging Technology Observatory"
```

By default, the script writes data to `CSET_Staff.csv`. To specify your own output file, add the `--output-filename` flag to the command, followed by a filename ending in .csv, like so:

```
python -m main --teams "Data Science,Emerging Technology Observatory" --output-filename my_filename.csv
```

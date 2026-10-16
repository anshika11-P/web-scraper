# Web Scraper for Headlines

## About the Project
A Python-based web scraping application that extracts news headlines and their URLs from a webpage and saves the collected data in JSON or CSV format.

## Features
- Extract headlines from webpages
- Collect available headline URLs
- Filter headlines using keywords
- Export results to JSON or CSV
- Handle request errors and log messages
- Check website scraping rules using robots.txt

## Technologies Used
- Python
- Requests
- BeautifulSoup
- JSON
- CSV

## Installation
Install the required libraries:

```bash
python -m pip install requests beautifulsoup4
```

## Usage

Save results as JSON:

```bash
python scraper.py --url "https://www.python.org/blogs/" --output headlines.json
```

Save results as CSV:

```bash
python scraper.py --url "https://www.python.org/blogs/" --output headlines.csv
```

Filter headlines by keyword:

```bash
python scraper.py --url "https://www.python.org/blogs/" --output filtered_news.json --keyword Python
```

## Output
The application saves extracted headline data in JSON or CSV format.

## Note
The extracted information depends on the website's HTML structure and published scraping rules. Some headlines may not have associated links or publication times.

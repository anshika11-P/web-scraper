
import requests
from bs4 import BeautifulSoup
import json
import csv
import argparse
import logging
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def scrape_headlines(url, keyword=None):
    """Fetch headlines from a news webpage."""

    # Check robots.txt
    robots_url = urljoin(url, "/robots.txt")
    robot_parser = RobotFileParser()
    robot_parser.set_url(robots_url)

    try:
        robot_parser.read()
        if not robot_parser.can_fetch("*", url):
            logging.error("Scraping is not allowed by robots.txt.")
            return []
    except Exception as error:
        logging.warning(f"Could not check robots.txt: {error}")
        logging.warning("Proceeding only if the site's published rules permit access.")

    headers = {
        "User-Agent": "EducationalHeadlineScraper/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        logging.error(f"Website request failed: {error}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        title = tag.get_text(" ", strip=True)

        if not title:
            continue

        link_tag = tag.find("a") or tag.find_parent("a")
        link = (
            urljoin(url, link_tag.get("href", ""))
            if link_tag else ""
        )

        if keyword and keyword.lower() not in title.lower():
            continue

        headlines.append({
            "title": title,
            "url": link,
            "time": ""
        })

    # Remove duplicate titles
    unique = []
    seen = set()

    for item in headlines:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique.append(item)

    return unique


def save_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def save_csv(data, output_file):
    with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file, fieldnames=["title", "url", "time"]
        )
        writer.writeheader()
        writer.writerows(data)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch headlines and save them to JSON or CSV."
    )
    parser.add_argument("--url", required=True, help="News webpage URL")
    parser.add_argument("--output", default="headlines.json",
                        help="Output filename ending in .json or .csv")
    parser.add_argument("--keyword", help="Optional headline keyword")
    args = parser.parse_args()

    headlines = scrape_headlines(args.url, args.keyword)

    if not headlines:
        logging.warning("No headlines found. The page may use JavaScript or different HTML tags.")
        return

    try:
        if args.output.lower().endswith(".json"):
            save_json(headlines, args.output)
        elif args.output.lower().endswith(".csv"):
            save_csv(headlines, args.output)
        else:
            logging.error("Output filename must end with .json or .csv")
            return
    except OSError as error:
        logging.error(f"Could not save the file: {error}")
        return

    print(f"\nFound {len(headlines)} headlines:\n")

    for number, item in enumerate(headlines, start=1):
        print(f"{number}. {item['title']}")
        print(f"   URL: {item['url'] or 'No link found'}")
        print(f"   Time: {item['time'] or 'Not available'}\n")

    logging.info(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()

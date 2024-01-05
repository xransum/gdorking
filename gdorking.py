#!/usr/bin/env python
import argparse
import logging
import random
import re
import sys
import urllib.parse

from typing import Any, Dict

import requests
import urllib3
from bs4 import BeautifulSoup


def encode_url(url: str) -> str:
    """Encodes a url.

    Args:
        url (str): The url to encode.

    Returns:
        (str): The encoded url.
    """
    # parse over the url, encoding the query params.
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    encoded_query_params = urllib.parse.urlencode(query_params, doseq=True)
    encoded_url = urllib.parse.urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            encoded_query_params,
            parsed_url.fragment,
        )
    )
    return encoded_url


__version__ = "0.0.1"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]
EXPLOIT_DB_ENDPOINT = "https://www.exploit-db.com"
GOOGLE_DORKING_EXPLOIT_DB_ENDPOINT = (
    f"{EXPLOIT_DB_ENDPOINT}/google-hacking-database"
)
EXPLOIT_DB_ENTRY_ENDPOINT = f"{EXPLOIT_DB_ENDPOINT}/ghdb/{'%s'}"
REQUEST_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "deflate, gzip, br",
    "Accept-Language": "en-US",
    "User-Agent": random.choice(USER_AGENTS),
    "X-Requested-With": "XMLHttpRequest",
}
EXCLUSION_CHARS = [" ", "."]

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def fetch_exploit_db_entry(entry_id: str) -> Dict[Any, Any]:
    """Fetches an exploit db entry.

    Args:
        entry_id (str): The exploit db entry id.

    Returns:
        (dict): The results containing the exploit db entry.
    """
    logger.debug(f"[+] Requesting URL: {EXPLOIT_DB_ENTRY_ENDPOINT % entry_id}")
    resp = None
    try:
        resp = requests.get(
            EXPLOIT_DB_ENTRY_ENDPOINT % entry_id,
            headers=REQUEST_HEADERS,
            timeout=10,
        )
    except requests.exceptions.SSLError:
        requests.packages.urllib3.disable_warnings()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            resp = requests.get(
                EXPLOIT_DB_ENTRY_ENDPOINT % entry_id,
                headers=REQUEST_HEADERS,
                timeout=10,
                verify=False,
            )
        except requests.exceptions.SSLError:
            logger.error(
                f"[-] Error fetching data from: {EXPLOIT_DB_ENTRY_ENDPOINT % entry_id}"
            )

    results = None
    if resp is None or resp.status_code != 200:
        logger.error(
            f"[-] Error fetching data from: {EXPLOIT_DB_ENTRY_ENDPOINT % entry_id}"
        )
    else:
        soup = BeautifulSoup(resp.text, "html.parser")
        ghdb_id = soup.select_one(
            ".statistics > .info > .row > .col-6:-soup-contains('GHDB-ID:') > h6.stats-title"
        )
        author = soup.select_one(
            ".statistics > .info > .row > .col-6:-soup-contains('Author:') > h6.stats-title"
        )
        publish_date = soup.select_one(
            ".card-stats .card-footer:-soup-contains('Published:') .stats"
        )
        google_search_url = soup.select_one(
            "div:-soup-contains('Google Search:') > a.external"
        )
        code_text = soup.select_one(".content code.language-text")
        if ghdb_id is None:
            logger.error(
                f"[-] Error fetching data from: {EXPLOIT_DB_ENTRY_ENDPOINT % entry_id}"
            )

        results = {
            "ghdb_id": ghdb_id.text.strip(),
            "author": author.text.strip(),
            "publish_date": publish_date.text.strip().split(": ")[-1],
            "google_search_url": encode_url(google_search_url["href"]),
            "code_text": code_text.text.strip(),
        }

    return results


def fetch_google_dorks() -> Dict[Any, Any]:
    """Fetches exploit db results for all google dorks entries.

    Data Source: https://www.exploit-db.com/google-hacking-database

    Args:
        None

    Returns:
        (dict): The results containing all of the google dork entries.
    """
    logger.debug(f"[+] Requesting URL: {GOOGLE_DORKING_EXPLOIT_DB_ENDPOINT}")
    resp = None
    try:
        resp = requests.get(
            GOOGLE_DORKING_EXPLOIT_DB_ENDPOINT,
            headers=REQUEST_HEADERS,
            timeout=10,
            allow_redirects=True,
        )
    except requests.exceptions.SSLError:
        requests.packages.urllib3.disable_warnings()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            resp = requests.get(
                GOOGLE_DORKING_EXPLOIT_DB_ENDPOINT,
                headers=REQUEST_HEADERS,
                timeout=10,
                verify=False,
                allow_redirects=True,
            )
        except requests.exceptions.SSLError:
            logger.error(
                f"[-] Error fetching data from: {GOOGLE_DORKING_EXPLOIT_DB_ENDPOINT}"
            )

    results = None
    if resp is None or resp.status_code != 200:
        logger.error(
            f"[-] Error fetching data from: {GOOGLE_DORKING_EXPLOIT_DB_ENDPOINT}"
        )
    else:
        # Extract json data from response.
        try:
            resp_json = resp.json()
        except ValueError:
            logger.error(
                f"[-] Error parsing json data from: {GOOGLE_DORKING_EXPLOIT_DB_ENDPOINT}"
            )
            print(resp.text)
            return

        # Pagination variables.
        total_records = resp_json["recordsTotal"]
        data = resp_json["data"]

        results = []  # List to store all extracted.

        # Loop through dorks, collecting and organizing them.
        for dork in data:
            # Extract the URL title from the html.
            soup = BeautifulSoup(dork["url_title"], "html.parser")
            # Use strip() to remove leading and trailing whitespace.
            extracted = soup.find("a").contents[0].strip()

            # For dorks that start with a capital letter, remove it.
            if re.search(r"^(Re|Fwd?):", extracted):
                extracted = re.sub(r"^(Re|Fwd?):", "", extracted)

            # Get all non-alphanumeric characters, excluding the ones in the
            # exclusion_chars list, these are characters that are allowed to
            # typically associated with a dork.
            non_alpha_num_chars = [
                c
                for c in re.findall(r"\W", extracted)
                if c not in EXCLUSION_CHARS
            ]

            # If there are no non-alphanumeric characters, then we can check
            # if the dork has any of the exceptions for the exclusion_chars.
            if len(non_alpha_num_chars) == 0:
                # Check if there are any periods that are not the last
                # character or the end of a possible sentence.
                if re.search(r"\.(?!\s|$)", extracted) is None:
                    # If there are, then we bail out
                    continue

            # Add the extracted dork to the list.
            results.append(extracted)

    # Sort the results.
    results = sorted(results)
    return results


def main() -> None:
    """Main caller function."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(f"gdorker v{__version__}"),
        epilog=(
            f"gdorker v{__version__}: Fetching the latest entries "
            "from the exploit-db website "
            "https://www.exploit-db.com/google-hacking-database."
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
    )
    parser.add_argument(
        "-i",
        "--id",
        dest="id",
        type=int,
        help="ID of the entry to fetch.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Enable debug logging.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        help="Output results to a file.",
    )
    args = parser.parse_args()

    # Set the logging level.
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Check if the id is specified.
    if args.id:
        logger.debug(f"[*] Fetching results for id: {args.id}")

        results = fetch_exploit_db_entry(args.id)

        # Create the text to print or write to a file.
        if results is not None:
            code_text = "\n".join(
                [line.rstrip() for line in results["code_text"].split("\n")]
            )
            code_width = max([len(line) for line in code_text.split("\n")])
            text = "\n".join(
                [
                    f"GHDB ID: {results['ghdb_id']}",
                    f"Exploit DB: {EXPLOIT_DB_ENTRY_ENDPOINT % args.id}",
                    f"Author: {results['author']}",
                    f"Publish Date: {results['publish_date']}",
                    f"Google Search URL: {results['google_search_url']}",
                    "- Code Text ".ljust(code_width, "-"),
                    code_text,
                    "-" * code_width,
                ]
            )

        # Write the results to a file if specified.
        if args.output:
            with open(args.output, "w", encoding="utf8") as f:
                f.write(text)
        else:
            print(text)

    # Check if the category is specified.
    else:
        logger.debug("[*] Fetching exploit-db data.")

        # Fetch the google dorks.
        results = fetch_google_dorks()
        text = ""

        # Create the text to print or write to a file.
        if results is not None:
            text = "\n".join(results)

        # Write the results to a file if specified.
        if args.output:
            with open(args.output, "w", encoding="utf8") as f:
                f.write(text)

        else:
            print(text)


# If the script is being executed directly, run the main function.
if __name__ == "__main__":
    main()

"""Driver module for gdorking."""

import csv
import json
import logging
import os

import requests
import urllib3
from bs4 import BeautifulSoup
from retry import retry

from gdorking import get_data_path

requests.packages.urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OUTPUT_FILE = os.path.join(get_data_path(), "google-dorks")
SUPPORTED_FILE_FORMATS = ["txt", "md", "json", "csv"]
OUTPUT_FILE_PATHS = {ff: f"{OUTPUT_FILE}.{ff}" for ff in SUPPORTED_FILE_FORMATS}

EXPLOIT_DB_ENDPOINT = "https://www.exploit-db.com"
EXPLOIT_DB_GOOGLE_DORKING_ENDPOINT = (
    f"{EXPLOIT_DB_ENDPOINT}/google-hacking-database"
)


@retry((urllib3.exceptions.HTTPError), delay=1, backoff=2)
def fetch_page(url: str, is_json=False) -> str:
    """Fetch a page from a URL.

    Args:
        url (str): The URL to fetch.
        is_json (bool, optional): Whether the response is JSON. Defaults to False.

    Raises:
        urllib3.exceptions.HTTPError: If the request fails.

    Returns:
        str: The response from the URL.
    """
    logging.debug(f"Fetching URL {url!r}")

    request = requests.get(
        url,
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "deflate, gzip, br",
            "Accept-Language": "en-US",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            ),
            "X-Requested-With": "XMLHttpRequest",
        },
        timeout=10,
        verify=False,
    )
    request.raise_for_status()
    if request.status_code != 200:
        raise urllib3.exceptions.HTTPError(
            f"Failed to fetch {url!r}. Status code: {request.status_code}"
        )

    if (
        request.headers.get("Content-Type") == "application/json"
        or is_json is True
    ):
        return json.loads(request.text)

    return request.text


def get_exploit_db_data() -> list:
    """Get the results from the Exploit DB Google Dorking page.

    Returns:
        (list): The results from the Exploit DB Google Dorking page.
    """
    logging.info("Fetching Exploit DB results")

    results = []
    page_limit = 250
    start_offset = 0

    while True:
        api_results = fetch_page(
            EXPLOIT_DB_GOOGLE_DORKING_ENDPOINT
            + f"?length={page_limit}&start={start_offset}",
            is_json=True,
        )
        records_total = api_results["recordsTotal"]
        data = api_results["data"]
        results.extend(data)

        if len(results) >= records_total:
            break

        start_offset += page_limit

    return results


def normalize_data(data: list) -> list:
    """Normalize the data from the Exploit DB Google Dorking page.

    Args:
        data (list): The data from the Exploit DB Google Dorking page.

    Returns:
        (list): The normalized data.
    """
    for dork in sorted(data, key=lambda x: int(x["id"])):
        url_title = soupify_html(dork.get("url_title", ""))

        dork["url"] = f"{EXPLOIT_DB_ENDPOINT}{url_title.a['href']}"
        dork["title"] = url_title.a.get_text()

    return data


def soupify_html(html: str) -> BeautifulSoup:
    """Create a BeautifulSoup object from HTML.

    Args:
        html (str): The HTML to parse.

    Returns:
        (BeautifulSoup): The BeautifulSoup object.
    """
    return BeautifulSoup(html, "html.parser")


def write_output_data(data: list, file_format: str) -> None:
    """Write the output data to a file.

    Args:
        data (list): The data to write.
        file_format (str): The file format to write the data in.
    """

    if file_format not in SUPPORTED_FILE_FORMATS:
        raise ValueError(
            f"Unsupported file format {file_format!r}. "
            f"Supported formats are {SUPPORTED_FILE_FORMATS}"
        )

    output_file = OUTPUT_FILE_PATHS[file_format]
    if file_format == "txt":
        with open(output_file, "w") as f:
            for dork in sorted(data, key=lambda x: x["title"]):
                f.write(f"{dork['title']}\n")

    elif file_format == "md":
        with open(output_file, "w") as f:
            f.write("# Google Dorks\n\n")

            categories = sorted(
                set(dork["category"]["cat_title"] for dork in data)
            )
            f.write("Table of Contents\n")
            f.write(
                "\n".join(
                    [
                        f"- [{category}](#{category.lower().replace(' ', '-')})"
                        for category in categories
                    ]
                )
                + "\n\n"
            )

            for category in categories:
                f.write(f"## {category}\n")
                for dork in sorted(data, key=lambda x: x["title"]):
                    if dork["category"]["cat_title"] == category:
                        f.write(f"- [{dork['title']}]({dork['url']})\n")
                f.write("\n")

    elif file_format == "json":
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)

    elif file_format == "csv":
        headers = [
            "id",
            "title",
            "url",
            "category",
            "date",
            "author",
        ]
        csv_data = [
            {
                "id": dork["id"],
                "title": dork["title"],
                "url": dork["url"],
                "category": dork["category"]["cat_title"],
                "date": dork["date"],
                "author": dork["author"]["name"],
            }
            for dork in data
        ]

        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(csv_data)

    else:
        raise ValueError(
            f"Supported file format {file_format!r}, but not implemented."
        )


def main() -> None:
    """Main function for gdorking."""
    results = get_exploit_db_data()
    data = normalize_data(results)

    for file_format in SUPPORTED_FILE_FORMATS:
        write_output_data(data, file_format)


if __name__ == "__main__":
    main()

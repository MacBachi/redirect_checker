#!/usr/bin/env python3

import requests
import argparse
import logging
import sys
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from colorama import init, Fore, Style

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Suppress retry log messages
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

# Initialize colorama
init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Define maximum number of redirects
MAX_REDIRECTS = 5

def create_session_with_redirect_limit(max_redirects):
    session = requests.Session()
    retry = Retry(
        total=max_redirects,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def check_redirect(url, show_history=False, filter_redirect=None, include_redirect=None, parsable=False, unique_targets=None):
    session = create_session_with_redirect_limit(MAX_REDIRECTS)
    try:
        response = session.head(url, allow_redirects=True, verify=False, timeout=10)
        history = response.history if show_history else []

        normalized_initial_url = url.rstrip('/')
        normalized_final_url = response.url.rstrip('/')

        is_http_to_https = (
            normalized_initial_url.startswith("http://")
            and normalized_final_url.startswith("https://")
            and normalized_initial_url[7:] == normalized_final_url[8:]
        )

        if parsable:
            if normalized_final_url != normalized_initial_url:
                if filter_redirect and normalized_final_url == filter_redirect.rstrip('/'):
                    return
                if include_redirect and normalized_final_url != include_redirect.rstrip('/'):
                    return
                if unique_targets is not None:
                    if normalized_final_url not in unique_targets:
                        unique_targets.add(normalized_final_url)
                        print(normalized_final_url)
            else:
                if unique_targets is not None:
                    if normalized_final_url not in unique_targets:
                        unique_targets.add(normalized_final_url)
                        print(normalized_final_url)
        else:
            if normalized_final_url != normalized_initial_url:
                if filter_redirect and normalized_final_url == filter_redirect.rstrip('/'):
                    return
                if include_redirect and normalized_final_url != include_redirect.rstrip('/'):
                    return
                if is_http_to_https:
                    result = f"{Fore.LIGHTBLACK_EX}[-] {url} -> {response.url}{Style.RESET_ALL}"
                else:
                    result = f"{Fore.GREEN}[+] {url} -> {response.url}{Style.RESET_ALL}"
            else:
                result = f"{Fore.RED}[-] {url} -> {response.url}{Style.RESET_ALL}"

            if show_history and history:
                history_info = " -> ".join(
                    [f"{resp.url} ({resp.status_code})" for resp in history]
                )
                result += f" | History: {history_info} -> {response.url} ({response.status_code})"

            logging.info(result)

    except requests.exceptions.RequestException:
        pass  # Suppress any request exceptions

def main():
    parser = argparse.ArgumentParser(description='Check URL for redirects.')
    parser.add_argument('url', nargs='?', help='The URL to check for redirects')
    parser.add_argument('-s', '--showredir', action='store_true', help='Show redirection history')
    parser.add_argument('-f', '--filter', help='Filter out specific redirection destination')
    parser.add_argument('-i', '--include', help='Include only specific redirection destination')
    parser.add_argument('-p', '--parsable', action='store_true', help='Show only the final redirection target')
    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    else:
        if not sys.stdin.isatty():
            urls = [line.strip() for line in sys.stdin]
        else:
            urls = [input("Enter the URL to check for redirects: ")]

    unique_targets = set()
    for url in urls:
        check_redirect(url, show_history=args.showredir, filter_redirect=args.filter, include_redirect=args.include, parsable=args.parsable, unique_targets=unique_targets)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3

import requests
import argparse
import logging
import sys
import urllib3
from colorama import init, Fore, Style

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def check_redirect(url, show_history=False, filter_redirect=None, include_redirect=None):
    try:
        # Send a HEAD request to the URL to check for redirects, without verifying SSL certificate
        response = requests.head(url, allow_redirects=True, verify=False)

        # Gather the redirection history
        history = response.history if show_history else []

        # Normalize URLs by removing trailing slashes
        normalized_initial_url = url.rstrip('/')
        normalized_final_url = response.url.rstrip('/')

        # Check for HTTP to HTTPS redirect
        is_http_to_https = normalized_initial_url.startswith("http://") and normalized_final_url.startswith("https://") and normalized_initial_url[7:] == normalized_final_url[8:]

        # Determine if there is a redirect and prepare the output
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
            history_info = " -> ".join([f"{resp.url} ({resp.status_code})" for resp in history])
            result += f" | History: {history_info} -> {response.url} ({response.status_code})"

        logging.info(result)

    except requests.exceptions.SSLError:
        logging.error(f"{Fore.YELLOW}[!] {url} -> Certificate Error{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{Fore.RED}[!] {url} -> Error: {e}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='Check URL for redirects.')
    parser.add_argument('url', nargs='?', help='The URL to check for redirects')
    parser.add_argument('-s', '--showredir', action='store_true', help='Show redirection history')
    parser.add_argument('-f', '--filter', help='Filter out specific redirection destination')
    parser.add_argument('-i', '--include', help='Include only specific redirection destination')
    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    else:
        # Check if there is piped input
        if not sys.stdin.isatty():
            urls = [line.strip() for line in sys.stdin]
        else:
            urls = [input("Enter the URL to check for redirects: ")]

    for url in urls:
        check_redirect(url, show_history=args.showredir, filter_redirect=args.filter, include_redirect=args.include)

if __name__ == "__main__":
    main()

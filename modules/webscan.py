import asyncio
import os
import socket
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json
from core.config import Config
from colorama import Fore, Style

class WebScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.wordlist_file = os.path.join(Config.WORDLISTS_DIR, 'subdomain.txt')
        self.patterns_file = os.path.join(Config.PAYLOADS_DIR, 'patterns.json')
        self.subdomains = self.load_wordlist()
        self.patterns = self.load_patterns(self.patterns_file)

    def load_wordlist(self):
        try:
            with open(self.wordlist_file, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Wordlist file not found!{Style.RESET_ALL}")
            return []

    def load_patterns(self, pattern_file):
        patterns = []
        if not os.path.isfile(pattern_file):
            print(f"{Fore.RED}Error: Pattern file '{pattern_file}' not found..{Style.RESET_ALL}")
            return patterns
        try:
            with open(pattern_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "patterns" in data and isinstance(data["patterns"], list):
                    patterns = data["patterns"]
                else:
                    print(f"{Fore.RED}Error: Patterns not found or not in the correct format.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error reading patterns file: {e}{Style.RESET_ALL}")
        return patterns

    async def resolve_dns(self, subdomain):
        full_domain = f"{subdomain}.{self.domain}"
        try:
            socket.setdefaulttimeout(1)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
                result = so.connect_ex((full_domain, 80))
                if result == 0:
                    print(f"{Fore.GREEN}[+] Found subdomain: {full_domain}{Style.RESET_ALL}")
                    return full_domain
        except Exception as e:
            pass

    async def subdomain_enumeration(self):
        print(f"{Fore.RED}Starting subdomain enumeration...{Style.RESET_ALL}")
        tasks = [self.resolve_dns(subdomain) for subdomain in self.subdomains]
        return await asyncio.gather(*tasks)

    async def get_links(self, cur_url):
        links = set()
        try:
            response = requests.get(cur_url, timeout=10)
            if response.status_code == 200:
                b_soup = BeautifulSoup(response.text, "html.parser")
                for i in b_soup.find_all("a", href=True):
                    href = i.get("href")
                    full_url = urljoin(cur_url, href)
                    if self.test_url(full_url) and self.intrnal_url(self.base_url, full_url):
                        links.add(full_url)
                if links:
                    print(f"{Fore.GREEN}[*] Discovered links from {cur_url}:{Style.RESET_ALL}")
                    for link in links:
                        print(f" - {link}")
            return links
        except requests.exceptions.RequestException as error:
            print(f"{Fore.RED}Error fetching {cur_url}: {error}{Style.RESET_ALL}")
            return set()

    def test_url(self, url):
        parse = urlparse(url)
        return bool(parse.scheme) and bool(parse.netloc)

    def intrnal_url(self, url, url2):
        return urlparse(url).netloc == urlparse(url2).netloc

    def search_patterns(self, url):
        matches = []
        for pattern in self.patterns:
            if pattern in url:
                matches.append(pattern)
        return matches

    async def check_vulnerabilities(self, url):
        print(f"Checking URL: {url}")
        matches = self.search_patterns(url)
        if matches:
            print(f"{Fore.GREEN}Matches found for patterns: {', '.join(matches)} in URL: {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No matches found in URL: {url}{Style.RESET_ALL}")
        print("-" * 40)

    async def start_run(self):
        discovered_subdomains = await self.subdomain_enumeration()
        tasks = []

        for subdomain in discovered_subdomains:
            if subdomain: 
                links = await self.get_links(f"http://{subdomain}")
                for link in links:
                    tasks.append(self.check_vulnerabilities(link))

        await asyncio.gather(*tasks)

    def run(self):
        print(f"{Fore.RED}Starting scan for base URL: {self.base_url}{Style.RESET_ALL}")
        asyncio.run(self.start_run())

import re
import os
import json
from core.config import Config
from colorama import Fore, Style
from rich.console import Console,Text

class URLVulnerabilityChecker:
    def __init__(self, url_file):
        
        patterns_file = os.path.join(Config.PAYLOADS_DIR, 'patterns.json')
        self.patterns_file = patterns_file
        self.patterns = self.load_patterns(self.patterns_file)
        self.url_file = url_file

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

    def search_patterns(self, url):
        matches = []
        for pattern in self.patterns:
            if pattern in url:
                matches.append(pattern)
        return matches

    def run(self):
        console = Console()
        console.print(Text("""                     
                                  ____ _____ 
                                 / ___|  ___|
                                | |  _| |_   
                                | |_| |  _|  
                                 \____|_|    
                                                                
                        Developed by: Ibrahem abo kila
                        """, style="bold magenta"))
        if not os.path.isfile(self.url_file):
            print(f"{Fore.RED}Error: File '{self.url_file}' not found.{Style.RESET_ALL}")
            return
        try:
            with open(self.url_file, 'r', encoding='utf-8') as f:
                urls = f.readlines()
        except Exception as e:
            print(f"{Fore.RED}Error reading URL file: {e}{Style.RESET_ALL}")
            return
        for url in urls:
            url = url.strip()
            if url:
                print(f"Checking URL: {url}")
                matches = self.search_patterns(url)
                if matches:
                    print(f"{Fore.GREEN}Matches found for patterns: {', '.join(matches)} in URL: {url}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No matches found in URL: {url}{Style.RESET_ALL}")
                print("-" * 40)

def do_run(url_file):
    checker = URLVulnerabilityChecker(url_file=url_file)
    checker.run()

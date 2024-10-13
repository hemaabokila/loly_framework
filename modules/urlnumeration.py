from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import time
from colorama import Fore, Style

class URLEnumeration:
    def __init__(self, base_url, max_depth=2):
        self.base_url = base_url
        self.max_depth = max_depth
        self.visited = set()
        self.to_visit = [(self.norm_url(base_url), 0)]

    def test_url(self, url):
        parse = urlparse(url)
        return bool(parse.scheme) and bool(parse.netloc)

    def intrnal_url(self, url, url2):
        domain = urlparse(url).netloc
        domain2 = urlparse(url2).netloc
        return domain == domain2

    def norm_url(self, url):
        return url.rstrip('/')

    def get_links(self, cur_url):
        links = set()
        try:
            response = requests.get(cur_url, timeout=10)
            if response.status_code == 200:
                b_soup = BeautifulSoup(response.text, "html.parser")
                for i in b_soup.find_all("a", href=True):
                    href = i.get("href")
                    full_url = urljoin(cur_url, href)
                    normd_url = self.norm_url(full_url)
                    if self.test_url(normd_url) and self.intrnal_url(self.base_url, normd_url):
                        links.add(normd_url)
                if links:
                    print(f"{Fore.GREEN}[*] Discovered links:{Style.RESET_ALL}")
                    for link in links:
                        print(f" - {link}")
            return links
        except requests.exceptions.RequestException as error:
            print(f"{Fore.RED}Error fetching {cur_url}: {error}{Style.RESET_ALL}")
            return set()

    def enum_url(self):
        print(f'''
        {Fore.RED}
                 _____ _   _ _   _ __  __ _   _ ____  _     
                | ____| \\ | | | | |  \\/  | | | |  _ \\| |    
                |  _| |  \\| | | | | |\\/| | | | | |_) | |    
                | |___| |\\  | |_| | |  | | |_| |  _ <| |___ 
                |_____|_| \\_|\\___/|_|  |_|\\___/|_| \\_\\_____|
                                                            
                        Developed by: Ibrahem abo kila
        {Style.RESET_ALL}
        ''')
        try:
            while self.to_visit:
                cur_url, depth = self.to_visit.pop()
                if cur_url not in self.visited and depth <= self.max_depth:
                    print(cur_url)
                    self.visited.add(cur_url)
                    new_links = self.get_links(cur_url)
                    for link in new_links:
                        normd_link = self.norm_url(link)
                        if normd_link not in self.visited and normd_link not in [x[0] for x in self.to_visit]:
                            self.to_visit.append((link, depth + 1))
                    time.sleep(1)
        except KeyboardInterrupt:
            print(f"{Fore.RED}Closed by user{Style.RESET_ALL}")

    def run(self):
        self.enum_url()

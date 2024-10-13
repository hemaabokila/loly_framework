import asyncio
import dns.resolver
from colorama import Fore, Style
import os
from core.config import Config

class SubdomainEnumeration:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = self.load_wordlist()

    def load_wordlist(self):
        try:
            wordlist_path = os.path.join(Config.WORDLISTS_DIR, 'subdomain.txt')
            with open(wordlist_path, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Wordlist file not found!{Style.RESET_ALL}")
            return []

    def wildcard(self):
        try:
            random_subdomain = f"random-{self.domain}"
            dns.resolver.resolve(random_subdomain, 'A')
            print(f"{Fore.GREEN}[-] Wildcard detected for {self.domain}{Style.RESET_ALL}")
            return True
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
            return False

    async def resolve_dns(self, subdomain, dis_subdomains, semaphore):
        full_domain = f"{subdomain}.{self.domain}"
        try:
            async with semaphore:
                dns.resolver.resolve(full_domain, 'A')
                dis_subdomains.append(full_domain)
                print(f"{Fore.GREEN}[+] Found subdomain: {full_domain}{Style.RESET_ALL}")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            pass

    async def main(self):
        print(f"""
                    {Fore.RED}
                     ____  _   _ ____  ____   ___  __  __    _    ___ _   _ 
                    / ___|| | | | __ )|  _ \ / _ \|  \/  |  / \  |_ _| \ | |
                    \___ \| | | |  _ \| | | | | | | |\/| | / _ \  | ||  \| |
                     ___) | |_| | |_) | |_| | |_| | |  | |/ ___ \ | || |\  |
                    |____/ \___/|____/|____/ \___/|_|  |_/_/   \_\___|_| \_|                                

                                Developed by: Ibrahem abo kila
                    {Style.RESET_ALL}

            """)

        if not self.subdomains:
            return

        if self.wildcard():
            print(f"{Fore.RED}Wildcard detected for {self.domain}. Stopping enumeration.{Style.RESET_ALL}")
            return

        semaphore = asyncio.Semaphore(Config.MAX_CONCURRENT_REQUESTS)
        dis_subdomains = []
        tasks = []
        for subdomain in self.subdomains:
            tasks.append(self.resolve_dns(subdomain, dis_subdomains, semaphore))

        await asyncio.gather(*tasks)

    def run(self):
        try:
            asyncio.run(self.main())
        except KeyboardInterrupt:
            print(f"{Fore.RED}\nExiting...{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] An error occurred: {e}{Style.RESET_ALL}")

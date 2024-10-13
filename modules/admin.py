import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.config import Config
import signal
from colorama import Fore, Style

class AdminPanel:
    def __init__(self, url,threads=10, timeout=5):
        
        wordlist_file = os.path.join(Config.WORDLISTS_DIR, 'admin.txt')
        self.wordlist_file = wordlist_file
        self.url = url.rstrip('/') 
        self.threads = threads 
        self.timeout = timeout  
        self.stop_requested = False 

        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        print(f"{Fore.RED}\nStopping execution...{Style.RESET_ALL}")
        self.stop_requested = True

    def is_url_reachable(self, url):
        try:
            response = requests.get(url, timeout=self.timeout)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def run(self):
        print(f'''
        {Fore.RED}
                        _    ____  __  __ ___ _   _   ____   _    _   _ _____ _     
                       / \  |  _ \|  \/  |_ _| \ | | |  _ \ / \  | \ | | ____| |    
                      / _ \ | | | | |\/| || ||  \| | | |_) / _ \ |  \| |  _| | |    
                     / ___ \| |_| | |  | || || |\  | |  __/ ___ \| |\  | |___| |___ 
                    /_/   \_\____/|_|  |_|___|_| \_| |_| /_/   \_\_| \_|_____|_____|
                                                                                    
                                    Developed by: Ibrahem abo kila 
        {Style.RESET_ALL}
        ''')
        if not self.is_url_reachable(self.url):
            print(f"{Fore.RED}Error: Unable to reach '{self.url}'{Style.RESET_ALL}")
            return

        try:
            with open(self.wordlist_file, "r", encoding="utf-8") as a_list:
                words = [line.strip() for line in a_list if line.strip()]

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = {executor.submit(self.check_url, word): word for word in words}

                for future in as_completed(futures):
                    if self.stop_requested:
                        print(f"{Fore.RED}Execution stopped by user.{Style.RESET_ALL}")
                        break
                    try:
                        future.result()
                    except Exception as e:
                        print(f"{Fore.RED}Error occurred: {e}{Style.RESET_ALL}")

        except FileNotFoundError:
            print(f"{Fore.RED}Error: Wordlist file '{self.wordlist_file}' not found.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error reading wordlist file: {e}{Style.RESET_ALL}")

    def check_url(self, word):
        end_url = f"{self.url}/{word}"
        if self.stop_requested:
            return
        try:
            response = requests.get(end_url, timeout=self.timeout)
            if response.status_code == 200:
                print(f"{Fore.GREEN}{end_url} :: found [++]{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{end_url} :: not found [--] (HTTP {response.status_code}){Style.RESET_ALL}")
        except requests.RequestException as e:
            print(f"{Fore.RED}{end_url} :: request error: {e}{Style.RESET_ALL}")

def do_run(url, threads=10, timeout=5):
    panel_checker = AdminPanel(url=url, threads=threads, timeout=timeout)
    panel_checker.run()




import requests
from bs4 import BeautifulSoup
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.config import Config
import os.path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecurityChecker():
    def __init__(self, url):
        self.url = url

    def load_file(self, file_name):
        try:
            if 'payload' in file_name:
                file_path = os.path.join(Config.PAYLOADS_DIR, file_name)
            elif 'wordlist' in file_name:
                file_path = os.path.join(Config.WORDLISTS_DIR, file_name)
            else:
                file_path = os.path.join(Config.CONFIGS_DIR, file_name)

            with open(file_path, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            logging.error(f"File not found: {file_name}")
            return []
        except Exception as e:
            logging.error(f"Error occurred while loading file {file_name}: {e}")
            return []

    def analyze_response(self):
        logging.info("Analyzing response for sensitive data leaks...")
        sensitive_patterns = self.load_file('key.txt')

        try:
            response = requests.get(self.url, timeout=Config.TIMEOUT)
            response.raise_for_status()
            found_keywords = [pattern for pattern in sensitive_patterns if re.search(pattern, response.text, re.IGNORECASE)]

            if found_keywords:
                logging.warning(f"Potential sensitive data leaks found: {', '.join(found_keywords)} in response.")
            else:
                logging.info("No sensitive data leaks detected.")

        except requests.exceptions.Timeout:
            logging.error("Request timed out while trying to connect.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while fetching the URL: {e}")

        logging.info("Response analysis completed.")

    def check_sql_injection(self):
        logging.info("Checking for SQL Injection vulnerabilities...")
        test_payloads = self.load_file('sqlpayloads.txt')

        for payload in test_payloads:
            try:
                response = requests.get(f"{self.url}{payload}", timeout=Config.TIMEOUT)

                if response.ok and re.search(r"(error|mysql|sql|syntax|database|query)", response.text, re.IGNORECASE):
                    logging.warning(f"Potential SQL Injection vulnerability found with payload: {payload.strip()}")
                    return
                logging.info(f"No SQL Injection vulnerability detected for payload: {payload.strip()}")

            except requests.exceptions.Timeout:
                logging.error("Request timed out while trying to connect.")
                break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred while fetching the URL: {e}")

        logging.info("SQL Injection check completed.")

    def check_xss(self):
        logging.info("Checking for XSS vulnerabilities...")
        test_payloads = self.load_file('xss_payloads.txt')

        for payload in test_payloads:
            try:
                response = requests.get(f"{self.url}?input={payload}", timeout=Config.TIMEOUT)

                if response.ok and payload in response.text:
                    logging.warning(f"Potential XSS vulnerability found with payload: {payload.strip()}")
                    return
                logging.info(f"No XSS vulnerability detected for payload: {payload.strip()}")

            except requests.exceptions.Timeout:
                logging.error("Request timed out while trying to connect.")
                break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred while fetching the URL: {e}")

        logging.info("XSS check completed.")

    def check_security_headers(self):
        logging.info("Checking for security headers...")
        try:
            response = requests.get(self.url, timeout=Config.TIMEOUT)
            security_headers = self.load_file('headers.txt')
            missing_headers = [header for header in security_headers if header not in response.headers]

            if missing_headers:
                logging.warning(f"Missing security headers: {', '.join(missing_headers)}")
            else:
                logging.info("All security headers are present.")

        except requests.exceptions.Timeout:
            logging.error("Request timed out while trying to connect.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while fetching the URL: {e}")

    def check_csrf_tokens(self):
        logging.info("Checking for CSRF tokens...")
        try:
            response = requests.get(self.url, timeout=Config.TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token_names = self.load_file('tokencsrf.txt')
            found_tokens = [token['value'] for name in csrf_token_names for token in soup.find_all('input', {'name': name}) if 'value' in token.attrs]

            if found_tokens:
                logging.info(f"CSRF token(s) found in the page: {', '.join(found_tokens)}")
            else:
                logging.warning("No CSRF token found in the page.")

        except requests.exceptions.Timeout:
            logging.error("Request timed out while trying to connect.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while fetching the URL: {e}")

    def check_ssrf(self):
        logging.info("Checking for SSRF vulnerabilities...")
        test_payloads = self.load_file('ssrf_payloads.txt')

        for payload in test_payloads:
            try:
                response = requests.get(f"{self.url}?url={payload}", timeout=Config.TIMEOUT)

                if response.ok and 'admin' in response.text.lower():
                    logging.warning(f"Potential SSRF vulnerability found with payload: {payload}")
                    return
                logging.info(f"No SSRF vulnerability detected for payload: {payload}")

            except requests.exceptions.Timeout:
                logging.error("Request timed out while trying to connect.")
                break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred while fetching the URL: {e}")

        logging.info("SSRF check completed.")

    def check_rce(self):
        logging.info("Checking for Remote Code Execution vulnerabilities...")
        test_payloads = self.load_file('rce_payloads.txt')

        for payload in test_payloads:
            try:
                response = requests.get(f"{self.url}?cmd={payload}", timeout=Config.TIMEOUT)

                if response.ok and 'root' in response.text.lower():
                    logging.warning(f"Potential RCE vulnerability found with payload: {payload}")
                    return
                logging.info(f"No RCE vulnerability detected for payload: {payload}")

            except requests.exceptions.Timeout:
                logging.error("Request timed out while trying to connect.")
                break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred while fetching the URL: {e}")

        logging.info("RCE check completed.")

    def check_command_injection(self):
        logging.info("Checking for Command Injection vulnerabilities...")
        test_payloads = self.load_file('command_injection_payloads.txt')

        for payload in test_payloads:
            try:
                response = requests.get(f"{self.url}?input={payload}", timeout=Config.TIMEOUT)

                if response.ok and 'expected_output' in response.text.lower():
                    logging.warning(f"Potential Command Injection vulnerability found with payload: {payload}")
                    return
                logging.info(f"No Command Injection vulnerability detected for payload: {payload}")

            except requests.exceptions.Timeout:
                logging.error("Request timed out while trying to connect.")
                break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred while fetching the URL: {e}")

        logging.info("Command Injection check completed.")

    def run(self):
        logging.info(f"Running security checks on: {self.url}")

        checks = [
            self.check_sql_injection,
            self.check_xss,
            self.check_security_headers,
            self.check_csrf_tokens,
            self.analyze_response,
            self.check_ssrf,
            self.check_rce,
            self.check_command_injection
        ]

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(check): check.__name__ for check in checks}
            try:
                for future in as_completed(futures):
                    check_name = futures[future]
                    try:
                       future.result()
                    except Exception as e:
                        logging.error(f"Error occurred in {check_name}: {e}")
            except KeyboardInterrupt:
                logging.warning("Process interrupted by user. Exiting...")


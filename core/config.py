import os

class Config:

    APP_NAME = "Loly Security Framework"
    VERSION = "1.0.0"
    WORDLISTS_DIR = os.path.join("wordlists")
    PAYLOADS_DIR = os.path.join("payloads")
    CONFIGS_DIR = os.path.join("configs")

    DEFAULT_WORDLIST_PATH = os.path.join(WORDLISTS_DIR, "subdomain.txt")
    ADMINPANEL_WORDLIST_PATH = os.path.join(WORDLISTS_DIR, "admin.txt")
    ANALYZE_RESPONSE_PATH=os.path.join(CONFIGS_DIR, "key.txt")
    SQL_PAYLOADS_PATH = os.path.join(PAYLOADS_DIR, "sqlpayloads.txt")
    XSS_PAYLOADS_PATH = os.path.join(PAYLOADS_DIR, "xss_payloads.txt")
    SSRF_PAYLOADS_PATH = os.path.join(PAYLOADS_DIR, "ssrf_payloads.txt")
    RCE_PAYLOADS_PATH = os.path.join(PAYLOADS_DIR, "rce_payloads.txt")
    COMMAND_INJECTION_PAYLOADS_PATH = os.path.join(PAYLOADS_DIR, "command_injection_payloads.txt")
    SECURITY_HEADERS_PATH = os.path.join(CONFIGS_DIR, "headers.txt")
    CSRF_TOKENS_PATH = os.path.join(CONFIGS_DIR, "tokencsrf.txt")
    PF_PAYLOADS_PATH = os.path.join(PAYLOADS_DIR, "patterns.json")
    

    TIMEOUT = 10 
    RETRIES = 3  

    LOGGING_LEVEL = "INFO"
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    MAX_CONCURRENT_REQUESTS = 50

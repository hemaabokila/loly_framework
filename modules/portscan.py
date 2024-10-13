import os
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

class PortScanner:
    def __init__(self, target, port=None,):
        self.target = target
        self.port = port

        self.ports = {
            20: "FTP Data Transfer",
            21: "FTP Control",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            67: "DHCP Server",
            68: "DHCP Client",
            69: "TFTP",
            80: "HTTP",
            110: "POP3",
            123: "NTP",
            137: "NetBIOS Name Service",
            138: "NetBIOS Datagram Service",
            139: "NetBIOS Session Service",
            143: "IMAP",
            161: "SNMP",
            194: "IRC",
            389: "LDAP",
            443: "HTTPS",
            445: "SMB",
            465: "SMTPS",
            514: "Syslog",
            515: "LPD",
            993: "IMAPS",
            995: "POP3S",
            1080: "SOCKS",
            1433: "Microsoft SQL Server",
            1434: "Microsoft SQL Monitor",
            1521: "Oracle Database",
            1723: "PPTP",
            3306: "MySQL",
            3389: "RDP",
            5060: "SIP",
            5432: "PostgreSQL",
            5900: "VNC",
            6379: "Redis",
            8080: "HTTP Proxy",
            8443: "HTTPS Proxy"
        }

    def tcp_port(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
            socket.setdefaulttimeout(1)
            try:
                result = so.connect_ex((self.target, port))
                if result == 0:
                    service = self.service_name(port)
                    print(f"{Fore.BLUE}TCP Port {port}: OPEN (Service: {service}){Style.RESET_ALL}")
            except Exception as e:
                print(f"Error scanning TCP port {port}: {e}")

    def service_name(self, port):
        return self.ports.get(port, "Unknown service")

    def ping_target(self):
        print(f'''
            {Fore.RED}
                 ____   ___  ____ _____   ____   ____    _    _   _ _   _ _____ ____  
                |  _ \ / _ \|  _ \_   _| / ___| / ___|  / \  | \ | | \ | | ____|  _ \ 
                | |_) | | | | |_) || |   \___ \| |     / _ \ |  \| |  \| |  _| | |_) |
                |  __/| |_| |  _ < | |    ___) | |___ / ___ \| |\  | |\  | |___|  _ < 
                |_|    \___/|_| \_\|_|   |____/ \____/_/   \_\_| \_|_| \_|_____|_| \_\
                                                          
                                    Developed by: Ibrahem abo kila
            {Style.RESET_ALL}
        ''')
        response = os.system(f"ping -c 1 {self.target}")
        if response == 0:
            print(f"{Fore.BLUE}{self.target} is up!{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}{self.target} is down or not reachable.{Style.RESET_ALL}")
            return False

    def run(self):
        try:
            if not self.ping_target():
                return
            
            print(f"Scanning {self.target} for open ports ...\n")


            scan_func = self.tcp_port
            ports_to_scan = self.ports.keys()

            
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(scan_func, i): i for i in ports_to_scan}
                for future in as_completed(futures):
                    pass 


        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Scan interrupted by user.{Style.RESET_ALL}")

def do_run(target):
    port_cheker = PortScanner(target=target)
    port_cheker.run()
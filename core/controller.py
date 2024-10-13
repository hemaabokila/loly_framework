from rich.console import Console
from modules.subdomain import SubdomainEnumeration
from modules.portscan import PortScanner
from modules.securitychecker import SecurityChecker
from modules.urlnumeration import URLEnumeration
from modules.ddos import DDoSAttack
from modules.gf import URLVulnerabilityChecker
from modules.admin import AdminPanel
from modules.webscan import WebScanner

console = Console()

module_map = {
    "subdomain": SubdomainEnumeration,
    "portscan": PortScanner,
    "scanall": SecurityChecker,
    "enumurl": URLEnumeration,
    "ddos": DDoSAttack,
    "gf": URLVulnerabilityChecker,
    "adminp": AdminPanel,
    "webscan": WebScanner,
}

def execute_module(module_name, target, *additional_args):
    module_class = module_map.get(module_name)
    
    if module_class:
        module_instance = module_class(target, *additional_args)
        module_instance.run()
    else:
        console.print(f"[bold red]Error: Tool '{module_name}' not found.[/bold red]")

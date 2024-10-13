
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cmd
from core.controller import execute_module
from rich.console import Console
from rich.table import Table
from rich.text import Text
from colorama import Fore, Style

console = Console()

class LolyFramework(cmd.Cmd):
    prompt = f"{Fore.BLUE}Loly >> {Style.RESET_ALL}"

    def __init__(self):
        super().__init__()
        self.display_welcome_message()
        self.display_available_tools()

    def display_welcome_message(self):
        console.print(Text("""
                                         _     ___  _  __   __
                                        | |   / _ \| | \ \ / /
                                        | |  | | | | |  \ V / 
                                        | |__| |_| | |___| |  
                                        |_____\___/|_____|_|  
                                    Developed by: Ibrahem abo kila                
                     _____ ____      _    __  __ _______        _____  ____  _  __
                    |  ___|  _ \    / \  |  \/  | ____\ \      / / _ \|  _ \| |/ /
                    | |_  | |_) |  / _ \ | |\/| |  _|  \ \ /\ / / | | | |_) | ' / 
                    |  _| |  _ <  / ___ \| |  | | |___  \ V  V /| |_| |  _ <| . \ 
                    |_|   |_| \_\/_/   \_\_|  |_|_____|  \_/\_/  \___/|_| \_\_|\_\
                                                                                          
                            http://github.com/hemaabokila/loly_framework
                                      ibrahemabokila@gmail.com
                           """, style="bold blue"))

    def display_available_tools(self):
        console.print("[bold blue]Available Tools:[/bold blue]")
        modules = [
            "subdomain - Subdomain Enumeration",
            "enumurl - URL Enumeration",
            "pf - URL Vulnerability Checker",
            "scanall - Security Checker",
            "webscan - Web scanner",
            "adminp - Admin panel fainder",
            "portscan - Port Scanner",
            "ddos - DDoSAttack",

        ]

        table = Table(title="[bold red]Tools[/bold red]")
        table.add_column("Tool Name", style="red", no_wrap=True)
        table.add_column("Description", style="blue")
        for module in modules:
            name, description = module.split(" - ")
            table.add_row(name, description)
        console.print(table)
    
    def do_run(self, arg):
        console.print("[bold blue]Running Tool...[/bold blue]")
        args = arg.split()
        if len(args) < 2:
            console.print("[bold red]Usage: run <tool_name> <target> [>> <output_file>][/bold red]")
            console.print("[bold red]Exampel: run enumurl http://example.com  >> urls.txt[/bold red]")
            return
        module_name = args[0]
        target = args[1]
        output_file = args[-1] if len(args) > 3 and args[-2] == '>>' else None
        additional_args = args[2:-2] if output_file else args[2:]
        try:
            if output_file:
                try:
                    with open(output_file, 'a') as f:
                        sys.stdout = f
                        execute_module(module_name, target, *additional_args)
                finally:
                    sys.stdout = sys.__stdout__
                console.print(f"[bold green]Output written to {output_file}[/bold green]")
            else:
                execute_module(module_name, target, *additional_args)
        except FileNotFoundError:
            console.print(f"[bold red]Error: The specified output file '{output_file}' could not be found.[/bold red]")
        except PermissionError:
            console.print(f"[bold red]Error: Permission denied for writing to '{output_file}'.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error executing module: {str(e)}[/bold red]")

    def do_exit(self, arg):
        "Exit the framework"
        console.print("Good bay...")
        return True

    def do_help(self, arg):
        console.print("[bold blue]Available Commands:[/bold blue]")
        console.print("[bold]run <tool_name> <target> [additional arguments] [>> <output_file>][/bold]")
        console.print("    Run a specific tool on the given target.")
        console.print("    - tool_name: Name of the tool to run (e.g., subdomain, portscan, scanall, enumurl).")
        console.print("    - <target>: Specify the target for the tool.")
        console.print("    - >> <output_file>: Optionally redirect output to a file.")

        console.print("\n[bold]Available Tools:[/bold]")
        console.print("[bold red]1. Subdomain Enumeration:[/bold red] Discover subdomains of a given domain.")
        console.print("    Usage: run subdomain <domain> [>> <output_file>]")
        console.print("    Example: run subdomain example.com >> subdomains.txt")

        console.print("[bold red]2. URL Enumeration:[/bold red] Enumerate URLs on the target.")
        console.print("    Usage: run enumurl <url> [>> <output_file>]")
        console.print("    Example: run enumurl http://example.com >> urls.txt")

        console.print("[bold red]3. Vulnerability Checker:[/bold red] URLs vulnerability checker on the target.")
        console.print("    Usage: run gf <urls_file> [>> <output_file>]")
        console.print("    Example: run gf urls.txt >> security_report.txt")

        console.print("[bold red]4. Security Checker:[/bold red] Perform a comprehensive security check on the target.")
        console.print("    Usage: run scanall <urls_file> [>> <output_file>]")
        console.print("    Example: run scanall urls.txt >> security_report.txt")

        console.print("[bold red]5. Web Scanner:[/bold red] Perform a comprehensive security check on the target.")
        console.print("    Usage: run wepscan <urls_file> [>> <output_file>]")
        console.print("    Example: run wpscan urls.txt >> security_report.txt")

        console.print("[bold red]6. Admin Panel:[/bold red] Admin panel fainder on the target.")
        console.print("    Usage: run adminp <url> [>> <output_file>]")
        console.print("    Example: run adminp http://example.com >> urls.txt")

        console.print("[bold red]7. Port Scanner:[/bold red] Scan a range of ports on the target.")
        console.print("    Usage: run portscan <url> or <ip> [>> <output_file>]")
        console.print("    Example: run portscan example.com or 192.168.1.1  >> ports.txt")

        console.print("[bold red]8. DDOS Attack:[/bold red] DDos attack on the target.")
        console.print("    Usage: run ddos <ip> ")
        console.print("    Example: run ddos 192.168.1.1 ")




        console.print("\n[bold]General Commands:[/bold]")
        console.print("[bold]exit[/bold]: Exit the framework.")
        console.print("[bold]help[/bold]: Display this help message.")





        console.print("[bold green]Developed by[/bold green]: [green]Ibrahem abo kila.[/green]")
        console.print("[bold green]Email[/bold green]: [green]Ibrahemabokila@gmail.com[/green]")

        console.print("\nFor detailed documentation on each tool, refer to the respective tool's documentation.")

def run():
    LolyFramework().cmdloop()

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("Good bay")


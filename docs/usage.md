# LolyFramework

**LolyFramework** is a security testing framework designed to make it easier for penetration testers and security enthusiasts to find vulnerabilities in web applications. It offers a variety of tools for subdomain enumeration, URL discovery, vulnerability checking, and more, all in one place.

## Features:
- Subdomain enumeration
- URL enumeration
- Vulnerability scanning (XSS, SQL injection, etc.)
- Web scanning and security checking
- Admin panel finder
- Port scanning
- DDoS simulation

## Getting Started

### Prerequisites
Before you begin, ensure you have the following installed on your system:

- **Python 3.6 or higher**
- Libraries listed in `requirements.txt` (these can be installed using the instructions below)

### Installation
Clone the repository to your local machine:

```bash
git clone https://github.com/hemaabokila/loly_framework
```

1. Navigate to the project directory:

```bash
cd loly-framework
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Run the framework:

```
python3 main.py
```
- Alternatively, to install the framework globally and run it directly using the command loly, you can use:

```
sudo pip install .
```
- After installation, simply run the framework with:

```
loly
```
## Usage
Once the framework is running, you can use the following commands within the framework:

## List of Tools
<div align="center">

| Tool Name | Description | Example Command |
|-----------|-------------|------------------|
| subdomain | Subdomain Enumeration | `run subdomain example.com >> subdomains.txt` |
| enumurl   | URL Enumeration | `run enumurl http://example.com >> urls.txt` |
| pf        | URL Vulnerability Checker | `run pf urls.txt >> vulnerabilities_report.txt` |
| scanall   | Security Checker | `run scanall urls.txt >> security_report.txt` |
| webscan   | Comprehensive Web Scanner | `run webscan urls.txt >> webscan_report.txt` |
| adminp    | Admin Panel Finder | `run adminp http://example.com >> adminpanels.txt` |
| portscan  | Port Scanner | `run portscan example.com >> ports.txt` |
| ddos      | DDoS Simulation | `run ddos 192.168.1.1` |

</div>

## Example Usage
To enumerate subdomains of example.com and save the output to a file:

```
run subdomain example.com >> subdomains.txt
```
To perform a full vulnerability check on URLs stored in a file urls.txt:

```
run scanall urls.txt >> security_report.txt
```
### Commands Overview
- run: Executes a specific tool against a target.
    - Usage: run <tool_name> <target> [>> <output_file>]
- exit: Exits the framework.
- help: Displays detailed information about available commands and tools.
## Available Tools
### Subdomain Enumeration
- Find subdomains associated with a domain.

```
run subdomain <domain> [>> <output_file>]
```
### URL Enumeration
- Enumerate URLs on a specified domain.

```
run enumurl <url> [>> <output_file>]
```
### Vulnerability Checker
- Check URLs for common vulnerabilities like XSS or SQL injection.

```
run pf <urls_file> [>> <output_file>]
```
### Security Checker
- Run a comprehensive security scan on a list of URLs.

```
run scanall <urls_file> [>> <output_file>]
```
### Web Scanner
- Perform detailed security scanning on web applications.

```
run webscan <urls_file> [>> <output_file>]
```
### Admin Panel Finder
- Scan for admin panel URLs on the target.

```
run adminp <url> [>> <output_file>]
```
### Port Scanner
- Scan open ports on a target domain or IP.

```
run portscan <url_or_ip> [>> <output_file>]
```
### DDoS Simulation
- Simulate a distributed denial-of-service (DDoS) attack.

```
run ddos <ip_address>
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
**Developed by Ibrahem Abo Kila**
- For any issues or inquiries, feel free to contact me:

- Email: ibrahemabokila@gmail.com
- GitHub: hemaabokila

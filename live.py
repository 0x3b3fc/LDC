import os
import requests
import socket
from concurrent.futures import ThreadPoolExecutor

# ANSI escape codes for text colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

MAX_RETRIES = 3
TIMEOUT = 5

def is_domain_live(domain):
    for _ in range(MAX_RETRIES):
        try:
            response = requests.head(f'http://{domain}', timeout=TIMEOUT)
            is_live = 200 <= response.status_code < 400
            status_color = GREEN if is_live else RED
            status = f'{status_color}Live{RESET}' if is_live else f'{RED}Not Working{RESET}'
            print(f"{domain} - {status}")
            return is_live
        except requests.RequestException:
            print(f"{domain} - {RED}Error: Unable to check status{RESET} (Retrying)")
        except socket.gaierror:
            print(f"{domain} - {RED}Error: DNS Resolution Failed{RESET}")
            break  # Break out of retry loop for DNS resolution errors

    print(f"{domain} - {RED}Max Retries Reached, Unable to Check{RESET}")
    return False

def filter_live_domains(input_file):
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_domains.txt")
    
    with open(input_file, 'r') as file:
        domains = file.read().splitlines()

    print("Checking domains:")
    
    # Using ThreadPoolExecutor for parallelization
    with ThreadPoolExecutor() as executor:
        live_domains = list(executor.map(is_domain_live, domains))

    live_domains = [domain for domain, is_live in zip(domains, live_domains) if is_live]

    with open(output_file, 'w') as file:
        file.write('\n'.join(live_domains))

if __name__ == "__main__":
    # Prompt the user for input file path
    input_file_path = input("Enter the path of the input file: ")

    filter_live_domains(input_file_path)
    print(f"Live domains filtered and saved to live_domains.txt in the same folder as the script.")
    print("Scan Finished")

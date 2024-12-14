
# Advanced WordPress Login Validator Script

This script is designed to validate WordPress login credentials by checking email and password combinations against WordPress login URLs. It supports multiple delimiters (`|`, `#`, `:`, and `@`) and ensures duplicate entries are skipped. Valid logins are saved instantly to a file.

**Created by [@mr_0x1](## Featureshttps://github.com/Mr-0x1)**  

## Features
- Supports multiple delimiters (`|`, `#`, `:`, `@`) for credentials.
- Automatically detects and formats lines into the standard format: `URL|Email|Password`.
- Validates credentials by attempting login requests.
- Removes duplicate entries to ensure each credential is processed only once.
- Saves valid logins instantly to an output file.
- Multi-threaded for faster processing using `ThreadPoolExecutor`.

## Prerequisites
Make sure you have the following installed:
- Python 3.x
- Required Python libraries:
  - `requests`
  - `concurrent.futures` (built-in with Python 3.x)
  - `termcolor`
  - `re` (built-in with Python 3.x)

To install missing dependencies, run:
```bash
pip install requests termcolor
```

## Usage

1. Clone or download this repository to your local machine :
  ```
git clone https://github.com/Mr-0x1/-wordpress-login-validator.git
   ```
3. Place your WordPress credentials file in the same directory as the script. Ensure the file contains lines in one of the following formats:
   ```
   http://example.com|email@example.com|password
   http://example.com#email@example.com#password
   http://example.com:email@example.com:password
   http://example.com@email@example.com@password
   ```
4. Run the script:
   ```bash
   python script_name.py
   ```
5. When prompted, enter the path to your credentials file.

   Example:
   ```
   Enter the path to your WordPress credentials file: credentials.txt
   ```

6. The script will process the file and save valid logins to `valid_logins.txt`.

## Output

- **Valid Credentials**: Saved in `valid_logins.txt` in the format `URL|Email|Password`.
- **Error Logs**: Errors encountered during processing (e.g., invalid format or unreachable URLs) are displayed in the terminal.

## Example Run

```plaintext
Advanced WordPress Login Validator Script
Enter the path to your WordPress credentials file: credentials.txt
[VALID] email@example.com | password at http://example.com
[INVALID] email2@example.com | wrongpassword at http://example.com
Validation complete. Valid logins saved to valid_logins.txt.
```

## Notes
- If the script encounters a domain resolution error, ensure the domain is reachable by visiting it in a browser or using tools like `ping` or `nslookup`.
- The script automatically adds `http://` to URLs if missing.

## Contributing

This project is maintained and created by [@mr_0x1](## Featureshttps://github.com/Mr-0x1).  
If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Credits

Created by [@Mr-0x1](## Featureshttps://github.com/Mr-0x1)

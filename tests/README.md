# Redirect Checker

A simple Python tool to check if a URL redirects and to what destination.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/redirect_checker.git
    cd redirect_checker
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

You can run the script directly from the command line. Ensure it is executable:

```sh
chmod +x redirect_checker.py
```

### Example Commands

1. **Check for redirects**:
    ```sh
    ./redirect_checker.py http://example.com
    ```

2. **Show redirection history**:
    ```sh
    echo -e "http://example.com\nhttp://github.com" | ./redirect_checker.py -s
    ```

3. **Filter out specific redirection**:
    ```sh
    echo -e "http://example.com\nhttp://github.com" | ./redirect_checker.py -f https://github.com/
    ```

4. **Include only specific redirection**:
    ```sh
    echo -e "http://example.com\nhttp://github.com" | ./redirect_checker.py -i https://github.com/
    ```

## Running Tests

To run the tests, use:
```sh
pytest tests/
```

## License

This project is licensed under the MIT License. 

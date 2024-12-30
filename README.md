# URL Shortener & UID Generator

## Description
This project will eventually implement a URL Shortener. It only implements a Unique ID Generator at the moment.
This project implements a Snowflake ID generator in Python. The Snowflake algorithm generates unique 64-bit integers (IDs) based on the current timestamp, datacenter ID, machine ID, and a sequence number.


## Features
- Generates unique 64-bit IDs
- Ensures IDs are sortable based on the timestamp
- Configurable datacenter and machine IDs

## TODO
- [ ] Implement URL Shortener
- [x] Create a command-line interface (CLI) for easier usage

## Technologies Used
- Python 3.x

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/tudorsonycx/simple-url-shortener.git
    ```
2. Navigate to the project directory:
    ```sh
    cd simple-url-shortener
    ```
3. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
5. Install the required dependencies (if any):
    ```sh
    pip install -r requirements.txt
    ```

## Usage
For now, it only supports Unique ID generation
1. Run the  script:
    ```sh
    python src/uid_gen.py
    ```
2. The script will continuously generate and print unique IDs.

## License
This project is licensed under the MIT [License](LICENSE)
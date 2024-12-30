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

To generate unique IDs using the Snowflake algorithm, use the following command:

```sh
python src/uid_gen.py [-h] [-g COUNT] [-s [FILENAME]] [-c FILENAME] [-p]
```

### Options

- `-g, --generate COUNT`: Generate `COUNT` unique IDs (default: 1).
- `-s, --save [FILENAME]`: Save the generated IDs to a JSON file and store in the `uids` directory (default: `uids.json`).
- `-c, --config FILENAME`: Path to the configuration file. Should be in a directory `config` (default: `config.json`).
- `-p, --print`: Whether to also print the IDs when saving.

### Examples

Generate 5 unique IDs and print them:

```sh
python src/uid_gen.py -g 5 -p
```

Generate 10 unique IDs, save them to `my_ids.json`, and print them:

```sh
python src/uid_gen.py -g 10 -s my_ids.json -p
```

Generate 3 unique IDs using a custom configuration file:

```sh
python src/uid_gen.py -g 3 -c my_config.json
```

## License
This project is licensed under the MIT [License](LICENSE)
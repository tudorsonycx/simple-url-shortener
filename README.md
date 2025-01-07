# URL Shortener & UID Generator

## Description
This project implements a URL Shortener and a Unique ID Generator.
The URL Shortener uses a Snowflake ID generator in Python to create unique short URLs.
The Snowflake algorithm generates unique 64-bit integers (IDs) based on the current timestamp, datacenter ID, machine ID, and a sequence number.

## Features
- Generates unique 64-bit IDs
- Ensures IDs are sortable based on the timestamp
- Configurable datacenter and machine IDs
- Shortens long URLs using Base 62 conversion
- Redirects short URLs to the original long URLs

## TODO
- [x] Implement URL Shortener
- [x] Create a command-line interface (CLI) for UID generator

## Technologies Used
- Python 3.x
- FastAPI
- SQLite

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
5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### URL Shortener API

Start the FastAPI server:

```sh
fastapi dev app.py
```

#### Endpoints

- `POST /shorten`: Shortens a given long URL.
    - Request body: `{"long_url": "http://example.com"}`
    - Response: `{"short_url": "abc123"}`

- `GET /{short_url}`: Redirects to the long URL corresponding to the given short URL.
    - Response: Redirects to the original long URL.

### Snowflake ID Generator

To generate unique IDs using the Snowflake algorithm, use the following command:

```sh
python src/uid_gen.py [-h] [-g COUNT] [-s [FILENAME]] [-c FILENAME] [-p]
```

#### Options

- `-g, --generate COUNT`: Generate `COUNT` unique IDs (default: 1).
- `-s, --save [FILENAME]`: Save the generated IDs to a JSON file and store in the `uids` directory (default: `uids.json`).
- `-c, --config FILENAME`: Path to the configuration file. Should be in a directory `config` (default: `config.json`).
- `-p, --print`: Whether to also print the IDs when saving.

#### Examples

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
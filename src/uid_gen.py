import time
import argparse
import json
import os
import sys


class Snowflake:
    """
    A class to generate unique IDs using the Snowflake algorithm.

    Attributes:
        epoch (int): The Twitter epoch timestamp in milliseconds.
        sequence (int): The sequence number to ensure uniqueness within the same millisecond.
        last_timestamp (int): The last timestamp when an ID was generated.
        datacenter_id_bits (int): The number of bits allocated for the datacenter ID.
        machine_id_bits (int): The number of bits allocated for the machine ID.
        sequence_bits (int): The number of bits allocated for the sequence number.
        max_datacenter_id (int): The maximum value for the datacenter ID.
        max_machine_id (int): The maximum value for the machine ID.
        max_sequence (int): The maximum value for the sequence number.
        timestamp_shift (int): The number of bits to shift the timestamp.
        datacenter_id_shift (int): The number of bits to shift the datacenter ID.
        machine_id_shift (int): The number of bits to shift the machine ID.
    """

    epoch = 1288834974657
    sequence = 0
    last_timestamp = 0

    datacenter_id_bits = 5
    machine_id_bits = 5
    sequence_bits = 12

    max_datacenter_id = 2 << datacenter_id_bits - 1
    max_machine_id = 2 << machine_id_bits - 1
    max_sequence = 2 << sequence_bits - 1

    timestamp_shift = datacenter_id_bits + machine_id_bits + sequence_bits
    datacenter_id_shift = machine_id_bits + sequence_bits
    machine_id_shift = sequence_bits

    def __init__(self, datacenter_id: int, machine_id: int) -> None:
        """
        Initialize the UID generator with the specified datacenter and machine IDs.

        Args:
            datacenter_id (int): The ID of the datacenter.
            machine_id (int): The ID of the machine.

        Raises:
            ValueError: If the datacenter_id is not between 0 and max_datacenter_id.
            ValueError: If the machine_id is not between 0 and max_machine_id.
        """
        if datacenter_id < 0 or datacenter_id > self.max_datacenter_id:
            raise ValueError(
                f"Datcenter ID must be between 0 and {self.max_datacenter_id}"
            )
        self.datacenter_id = datacenter_id
        if machine_id < 0 or machine_id > self.max_machine_id:
            raise ValueError(f"Machine ID must be between 0 and {self.max_machine_id}")
        self.machine_id = machine_id

    @classmethod
    def load_config(cls, config_file):
        """
        Load and validate the configuration from a JSON file.

        Args:
            config_file (str): The name of the configuration file to load.

        Returns:
            dict: The loaded configuration dictionary containing 'datacenter_id' and 'machine_id'.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the configuration file is not a valid JSON or does not contain the required keys.
        """
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "config", config_file
        )
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Configuration file '{config_file}' does not exist"
            )

        try:
            with open(config_path) as f:
                config = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(
                f"Configuration file '{config_file}' is not a valid JSON file"
            )

        valid_keys = {"datacenter_id", "machine_id"}
        if not valid_keys.issubset(config.keys()):
            raise ValueError(
                f"Config file '{config_file}' doesn't contain 'machine_id' and 'datacenter_id' keys"
            )

        return config

    def current_time(self) -> int:
        """
        Get the current time in milliseconds since the epoch.

        Returns:
            int: The current time in milliseconds.
        """
        return int(time.time() * 1000)

    def __wait_for_next_millisec(self, last_timestamp: int) -> int:
        """
        Waits until the next millisecond.

        This method continuously checks the current time until it is greater than the provided last timestamp.
        It ensures that the returned timestamp is always in the future relative to the last timestamp.

        Args:
            last_timestamp (int): The last recorded timestamp in milliseconds.

        Returns:
            int: The new timestamp in milliseconds, which is guaranteed to be greater than the last timestamp.
        """
        timestamp = self.current_time()
        while timestamp <= last_timestamp:
            timestamp = self.current_time()
        return timestamp

    def generate_id(self):
        """
        Generates a unique identifier based on the current timestamp, datacenter ID, machine ID, and sequence number.

        The method ensures that the generated ID is unique by incorporating the current timestamp, datacenter ID, machine ID, and a sequence number that increments if multiple IDs are generated within the same millisecond.

        Raises:
            Exception: If the system clock moves backwards, making the current timestamp less than the last recorded timestamp.

        Returns:
            int: A unique identifier.
        """
        timestamp = self.current_time()
        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Cannot generate id")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.max_sequence
            if self.sequence == 0:
                timestamp = self.__wait_for_next_millisec(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        id = (
            (timestamp - self.epoch) << self.timestamp_shift
            | (self.datacenter_id << self.datacenter_id_shift)
            | (self.machine_id << self.machine_id_shift)
            | self.sequence
        )

        return id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate unique IDs.")
    parser.add_argument(
        "-g",
        "--generate",
        type=int,
        default=1,
        metavar="COUNT",
        help="generate COUNT unique IDs",
    )
    parser.add_argument(
        "-s",
        "--save",
        nargs="?",
        const="uids.json",
        metavar="FILENAME",
        help="save the generated IDs to a JSON file and store in the "
        "'uids' directory (default: uids.json)",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.json",
        metavar="FILENAME",
        help="path to the configuration file. should be in a directory 'config'",
    )
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="whether to also print the IDs when saving",
    )
    args = parser.parse_args()

    try:
        config = Snowflake.load_config(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)
    datacenter_id = config["datacenter_id"]
    machine_id = config["machine_id"]

    try:
        uid_gen = Snowflake(datacenter_id, machine_id)
    except ValueError as e:
        print(e)
        sys.exit(1)

    uids = []

    for _ in range(args.generate):
        try:
            unique_id = uid_gen.generate_id()
        except Exception as e:
            print(e)
            sys.exit(1)

        uids.append(unique_id)
        if not args.save or args.print:
            print(f"Generated ID: {unique_id}")

    if args.save:
        uids_dir = os.path.join(os.path.dirname(__file__), "..", "uids")
        if not os.path.exists(uids_dir):
            os.makedirs(uids_dir)

        uid_path_base = os.path.basename(args.save)
        extension_idx = len(uid_path_base)
        if "." in uid_path_base:
            extension_idx = uid_path_base.find(".")
        uid_path_base_root = uid_path_base[:extension_idx]

        uids_output_path = os.path.join(uids_dir, f"{uid_path_base_root}.json")

        with open(uids_output_path, "w") as f:
            json.dump(uids, f, indent="\t")
            print(f"Saved {len(uids)} IDs to {uids_output_path}")

import time
import argparse


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
        if datacenter_id < 0 or datacenter_id > self.max_datacenter_id:
            raise ValueError(
                f"Datcenter ID must be between 0 and {self.max_datacenter_id}"
            )
        if machine_id < 0 or machine_id > self.max_machine_id:
            raise ValueError(f"Machine ID must be between 0 and {self.max_machine_id}")
        self.datacenter_id = datacenter_id
        self.machine_id = machine_id

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

        This method loops until the current timestamp is greater than the provided last_timestamp.
        It ensures that the next timestamp is always in the future compared to the last_timestamp.

        Args:
            last_timestamp (int): The last recorded timestamp.

        Returns:
            int: The new timestamp that is greater than the last_timestamp.
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
    args = parser.parse_args()

    uid_gen = Snowflake(1, 1)

    for _ in range(args.generate):
        unique_id = uid_gen.generate_id()
        print(f"Generated ID: {unique_id}")

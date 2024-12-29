import time


class Snowflake:
    epoch = 1288834974657
    sequence = 0
    last_timestamp = 0

    datacenter_id_bits = 5
    machine_id_bits = 5
    sequence_bits = 12

    max_datacenter_id = 2**datacenter_id_bits - 1
    max_machine_id = 2**machine_id_bits - 1
    max_sequence = 2**sequence_bits - 1

    timestamp_shift = datacenter_id_bits + machine_id_bits + sequence_bits
    datacenter_id_shift = machine_id_bits + sequence_bits
    machine_id_shift = sequence_bits

    def __init__(self, *, datacenter_id: int, machine_id: int) -> None:
        if datacenter_id < 0 or datacenter_id > self.max_datacenter_id:
            raise ValueError(
                f"Datcenter ID must be between 0 and {self.max_datacenter_id}"
            )
        if machine_id < 0 or machine_id > self.max_machine_id:
            raise ValueError(f"Machine ID must be between 0 and {self.max_machine_id}")
        self.datacenter_id = datacenter_id
        self.machine_id = machine_id

    def current_time(self) -> int:
        return int(time.time() * 1000)

    def __wait_for_next_millisec(self, last_timestamp: int) -> int:
        timestamp = self.current_time()
        while timestamp <= last_timestamp:
            timestamp = self.current_time()
        return timestamp

    def generate_id(self):
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
    snowflake = Snowflake(datacenter_id=1, machine_id=1)
    while True:
        print(snowflake.generate_id())
        choice = input("Generate another?: yes/no ").lower()
        if choice == "no":
            break

import string

CHARS_62 = string.digits + string.ascii_lowercase + string.ascii_uppercase


def encode_uid_62(uid: int) -> str:
    """
    Encodes a given integer UID into a base-62 string.

    Args:
        uid (int): The integer UID to encode.

    Returns:
        str: The base-62 encoded string representation of the UID.
    """
    encoded_chars = ""
    while uid:
        r = uid % 62
        encoded_chars = CHARS_62[r] + encoded_chars
        uid //= 62
    return encoded_chars

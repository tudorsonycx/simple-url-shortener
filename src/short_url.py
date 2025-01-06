import string

CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase


def encode_uid_62(uid: int) -> str:
    encoded_chars = ""
    while uid:
        r = uid % 62
        encoded_chars = CHARS[r] + encoded_chars
        uid //= 62
    return encoded_chars

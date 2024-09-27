import base64


def binary_to_b64(binary_str: bytes) -> str:
    """Converts binary data into base64"""
    return base64.b64encode(binary_str).decode("utf-8")


def b64_to_binary(b64_str: str) -> bytes:
    """Converts base64 strings in binary data"""
    return base64.b64decode(b64_str.encode("utf-8"))


def string_to_b64(input_string):
    """Converts python input string into base64"""
    # Convert the input string to bytes
    string_bytes = input_string.encode('utf-8')
    # Encode the bytes to base64
    base64_bytes = base64.b64encode(string_bytes)
    # Convert the base64 bytes back to a string
    base64_string = base64_bytes.decode('utf-8')
    return base64_string


def b64_to_string(base64_string):
    """Converts base64 string into python strings"""
    # Convert the base64 string to bytes
    base64_bytes = base64_string.encode('utf-8')
    # Decode the base64 bytes
    string_bytes = base64.b64decode(base64_bytes)
    # Convert the decoded bytes back to a string
    decoded_string = string_bytes.decode('utf-8')
    return decoded_string


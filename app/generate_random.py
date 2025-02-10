import secrets
import string

def generate_random(length=12, use_uppercase=True, use_digits=True, use_special_chars=False):
    """
    Generate a random string.

    :param length: Length of the random string. Default is 12.
    :param use_uppercase: Include uppercase letters. Default is True.
    :param use_digits: Include digits. Default is True.
    :param use_special_chars: Include special characters. Default is False.
    :return: A random string.
    """
    # Define the character set
    char_set = string.ascii_lowercase
    if use_uppercase:
        char_set += string.ascii_uppercase
    if use_digits:
        char_set += string.digits
    if use_special_chars:
        char_set += string.punctuation

    # Generate the random string
    return ''.join(secrets.choice(char_set) for _ in range(length))


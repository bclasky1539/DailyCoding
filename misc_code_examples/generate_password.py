"""
This python program will generate passwords.
Additional features can be added as needed.
"""

import secrets
import string


def generate_password(length: int, include_special: bool = True,
                      start_with_letter: bool = False) -> str:
    """
    Generate a random password of given length

    Args:
        param length: The length of the password.
        param include_special: The include special characters.
        param start_with_letter: The start with letter.

    Returns:
        str: The generated password as a string.
    """

    # Base character set always includes letters and digits
    input_chars: str = string.ascii_letters + string.digits

    # Add special characters if requested
    if include_special:
        input_chars += string.punctuation

    # The secrets module is specifically designed for security-sensitive functions
    # like generating passwords, making it the preferable way for this use case.
    if start_with_letter and length > 0:
        # First character must be a letter
        first_char = secrets.choice(string.ascii_letters)
        # Generate the rest of the password
        rest_of_password = ''.join(secrets.choice(input_chars) for _ in range(length - 1))
        gen_password: str = first_char + rest_of_password
    else:
        # Generate standard password
        gen_password = ''.join(secrets.choice(input_chars) for _ in range(length))

    return gen_password


def get_yes_no_input(prompt: str) -> bool:
    """
    Get a yes/no input from the user with validation.

    Args:
        prompt: The question to ask the user

    Returns:
        bool: True for yes, False for no
    """
    valid_responses = {'y': True, 'yes': True, 'n': False, 'no': False}

    while True:
        user_input = input(prompt).lower()
        if user_input in valid_responses:
            return valid_responses[user_input]

        print("Invalid input. Please enter 'y' or 'n'.")


def get_int_input(prompt: str, context: str = "min_length") -> int:
    """
    Get an integer input from the user with validation.

    Args:
        prompt: The question to ask the user
        context: What kind of value we're collecting ('length' or 'count')

    Returns:
        int: The validated integer input or context-specific default
    """
    # Different defaults for different contexts
    defaults: dict[str, int] = {
        "length": 16,  # Default length of password is 16
        "count": 5,  # Default count of passwords is 5
        "min_length": 8  # Default minimum length for secure passwords. This will affect the number
        # of passwords generated if the context is not specified
    }
    default: int = defaults.get(context, 10)  # 10 as fallback is still used

    # Minimum validation thresholds for specific contexts
    min_thresholds: dict[str, int] = {
        "length": 8,  # Minimum length of password must be at least 8
        "count": 1,  # Minimum number of passwords must be at least 1
        "min_length": 8  # Minimum length should be at least 8 for security
    }
    min_threshold = min_thresholds.get(context, 1)

    try:
        user_input: str = input(prompt)
        value = int(user_input)

        if value < min_threshold:
            print(f"Value must be at least {min_threshold}. Using default of {default}.")
            return default
        return value
    except ValueError:
        print(f"Using default of {default}.")
        return default


def main() -> None:
    """

    Return:
        None:
    """
    # Ask user how long the password should be
    length = get_int_input("Enter desired password length (Press Enter for default of 16): ",
                           context="length")
    # Ask user if they want the password to contain special characters
    include_special = get_yes_no_input("Include special characters? (y/n): ")
    # Ask user if they want the password to start with a letter
    start_with_letter = get_yes_no_input("Start with a letter? (y/n): ")
    # Ask user how many passwords should it generate
    numbers_of_passwords = get_int_input("How many passwords would you like to generate"
                                         " (Press Enter for default of 5)? ", context="count")

    # Generate and display password(s)
    print("\nGenerated Passwords:")
    print("-" * 30)
    for i in range(numbers_of_passwords):
        password = generate_password(length, include_special, start_with_letter)
        print(f"Password {i + 1}: {password}")
    print("-" * 30)


if __name__ == '__main__':
    main()

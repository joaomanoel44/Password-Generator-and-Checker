#!/usr/bin/env python3
# Shebang: allows direct execution of this file on Unix-like systems.

# Standard libraries for random selection, character classes, filesystem access,
# and program termination.
# Indentation normalised to 4 spaces throughout
import random  # for random choices of characters
import string  # predefined character sets (ascii_letters, digits, punctuation)
import os      # filesystem operations (create folders, join paths)
import sys     # access to interpreter functions (e.g. sys.exit)

# DATA_DIR: absolute path to the 'data' directory relative to the project
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
# PASSWORDS_FILE: full path to the file where generated passwords are appended.
PASSWORDS_FILE = os.path.join(DATA_DIR, 'passwords.txt')


def ensure_data_dir():
    """Ensure that DATA_DIR exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def save_password(password: str) -> None:
    """Append a password to the passwords file."""
    ensure_data_dir()
    with open(PASSWORDS_FILE, 'a', encoding='utf-8') as fh:
        fh.write(password + '\n')


def generate_password(length: int, include_special: bool) -> str:
    """Generate a random password."""
    if length < 8:
        raise ValueError('length must be at least 8')

    lower   = string.ascii_lowercase
    upper   = string.ascii_uppercase
    digits  = string.digits
    special = string.punctuation if include_special else ''
    pool    = lower + upper + digits + special

    chars = [
        random.choice(lower),   # at least one lowercase
        random.choice(upper),   # at least one uppercase
        random.choice(digits),  # at least one digit
    ]
    if include_special:
        chars.append(random.choice(special))  # at least one special char

    while len(chars) < length:
        chars.append(random.choice(pool))

    random.shuffle(chars)
    return ''.join(chars[:length])


def check_password_strength(password: str) -> str:
    """Classify password strength as Weak, Medium, or Strong."""
    has_upper   = any(c.isupper() for c in password)
    has_lower   = any(c.islower() for c in password)
    has_digit   = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    length     = len(password)
    categories = sum((has_upper, has_lower, has_digit, has_special))

    if length >= 12 and categories == 4:
        return 'Strong'
    if length >= 8 and categories >= 3:
        return 'Medium'
    return 'Weak'


def prompt_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """Prompt the user until a valid integer within the allowed range is entered."""
    while True:
        try:
            raw   = input(prompt).strip()
            value = int(raw)
            if min_value is not None and value < min_value:
                print(f'Input must be at least {min_value}.')
                continue
            if max_value is not None and value > max_value:  # Upper bound validation
                print(f'Input must be at most {max_value}.')
                continue
            return value
        except ValueError:
            print('Invalid input — please enter an integer.')


def prompt_yes_no(prompt: str) -> bool:
    """Ask the user a yes/no question and return True/False."""
    while True:
        raw = input(prompt + ' (y/n): ').strip().lower()
        if raw in ('y', 'yes'):
            return True
        if raw in ('n', 'no'):
            return False
        print('Please answer "y" or "n".')


def main() -> int:
    """Main loop of the console application."""
    print('Password Generator and Checker')
    try:
        while True:
            print('\nMenu:')
            print('1) Generate a new password')
            print('2) Check a password')
            print('3) Quit')
            choice = input('Choose an option [1-3]: ').strip()

            if choice == '1':
                print('Password length must be between 8 and 64 characters.')  # Inform user of valid range
                length          = prompt_int('Desired length (8-64): ', min_value=8, max_value=64)
                include_special = prompt_yes_no('Include special characters?')
                try:
                    pw = generate_password(length, include_special)
                except Exception as e:
                    print('Error generating password:', e)
                    continue
                save_password(pw)
                print('\nGenerated password:')
                print(pw)
                print(f'The password was appended to {PASSWORDS_FILE}.')

            elif choice == '2':
                pw = input('Enter the password to check: ').strip()
                if not pw:  # Guard: reject empty input before evaluating strength
                    print('No password entered.')
                    continue
                result = check_password_strength(pw)
                print(f'Strength: {result}')
                if result == 'Weak':  # Tip: guide the user towards a stronger password
                    print('Tip: try a password with at least 8 characters and a mix of uppercase, lowercase, digits and special characters.')

            elif choice == '3' or choice.lower() in ('q', 'quit', 'exit'):
                print('Exiting program.')
                break

            else:
                print('Invalid selection — please choose 1, 2 or 3.')

    except (KeyboardInterrupt, EOFError):
        print('\nProgram terminated.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
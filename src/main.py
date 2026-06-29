
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
# (one level above this file). Using os.path.abspath and os.path.join makes
# the path correct regardless of the current working directory.
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
# PASSWORDS_FILE: full path to the file where generated passwords are appended.
PASSWORDS_FILE = os.path.join(DATA_DIR, 'passwords.txt')


def ensure_data_dir():
    """Ensure that DATA_DIR exists.

    - os.makedirs with exist_ok=True creates directories recursively and does not
      raise an error if the directory already exists.
    """
    # Create the data directory if needed (no error if it already exists)
    os.makedirs(DATA_DIR, exist_ok=True)


def save_password(password: str) -> None:
    """Append a password to the passwords file.

    Flow:
    1. Ensure the data directory exists (ensure_data_dir).
    2. Open the file in append mode ('a') with UTF-8 encoding.
    3. Write the password followed by a newline.
    """
    # Ensure the directory exists before opening the file
    ensure_data_dir()
    # Open the file in append mode; if it doesn't exist it will be created
    with open(PASSWORDS_FILE, 'a', encoding='utf-8') as fh:
        # write password plus newline
        fh.write(password + '\n')


def generate_password(length: int, include_special: bool) -> str:
    """Generate a random password.

    Parameters:
    - length: desired length (function expects validated input >= 8)
    - include_special: whether to include special characters (e.g. '!@#')

    Behavior:
    - Ensure at least one character from each relevant category (lower, upper,
      digit, optional special) to avoid producing a password from a single category.
    - Fill the rest up to the requested length from the combined pool, then shuffle.
    """
    # Defensive check: abort if length is too small
    if length < 8:
        raise ValueError('length must be at least 8')

    # Define character sets
    lower = string.ascii_lowercase   # all lowercase letters
    upper = string.ascii_uppercase   # all uppercase letters
    digits = string.digits           # '0123456789'
    # Use punctuation only when include_special is True
    special = string.punctuation if include_special else ''

    # Combine the allowed characters into a single pool
    pool = lower + upper + digits + special

    # chars: list with required characters to cover categories
    chars = [
        random.choice(lower),  # at least one lowercase
        random.choice(upper),  # at least one uppercase
        random.choice(digits),  # at least one digit
    ]
    # If special characters requested, add one required special char
    if include_special:
        chars.append(random.choice(special))

    # Fill up to the requested length with random choices from the pool
    while len(chars) < length:
        chars.append(random.choice(pool))

    # Shuffle so required characters are not always at the start
    random.shuffle(chars)

    # Return a string of the exact requested length
    return ''.join(chars[:length])


def check_password_strength(password: str) -> str:
    """Classify password strength as 'Weak', 'Medium', or 'Strong'.

    Criteria (strict):
    - 'Strong' if length >= 12 AND all four categories are present
    - 'Medium' if length >= 8 AND at least three of the four categories are present
    - 'Weak' otherwise

    The function checks the four categories and counts how many are satisfied.
    """
    # Check presence of uppercase, lowercase, digits and special characters
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    # Password length
    length = len(password)

    # Number of satisfied categories (True==1, False==0)
    categories = sum((has_upper, has_lower, has_digit, has_special))

    # Evaluate according to the rules above
    if length >= 12 and categories == 4:
        return 'Strong'
    if length >= 8 and categories >= 3:
        return 'Medium'
    return 'Weak'


def prompt_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """Prompt the user until a valid integer is entered.

    - prompt: text shown to the user
    - min_value: if provided, ensure the value is >= min_value
    - max_value: if provided, ensure the value is <= max_value
    """
    while True:
        try:
            # input() reads a line from stdin
            raw = input(prompt).strip()
            # Try to convert the input into an integer
            value = int(raw)
            # If a minimum is specified, validate it
            if min_value is not None and value < min_value:
                print(f'Input must be at least {min_value}.')
                continue
            # Upper bound validation
            if max_value is not None and value > max_value:
                print(f'Input must be at most {max_value}.')
                continue
            # Return the valid integer
            return value
        except ValueError:
            # Error handling: do not raise, ask again
            print('Invalid input — please enter an integer.')


def prompt_yes_no(prompt: str) -> bool:
    """Ask the user a yes/no question and return True/False.

    Accepted answers (case-insensitive): 'y', 'yes', 'n', 'no'.
    On invalid input the question is repeated.
    """
    while True:
        raw = input(prompt + ' (y/n): ').strip().lower()
        if raw in ('y', 'yes'):
            return True
        if raw in ('n', 'no'):
            return False
        # If input wasn't recognized, prompt again
        print('Please answer "y" or "n".')


def main() -> int:
    """Main loop of the console application.

    - Shows a menu with three options: generate password, check password, quit.
    - Executes the selected action and stays in the loop until the user quits.
    """
    # Greeting / title
    print('Password Generator and Checker')
    try:
        # Infinite loop for the interactive menu
        while True:
            # Print the menu
            print('\nMenu:')
            print('1) Generate a new password')
            print('2) Check a password')
            print('3) Quit')
            # Read the user's choice and strip whitespace
            choice = input('Choose an option [1-3]: ').strip()

            # Option 1: Generate password
            if choice == '1':
                # Ask for length with validation (minimum 8, maximum 64)
                print('Password length must be between 8 and 64 characters.')  # Inform the user of the valid range before prompting
                length = prompt_int('Desired length (8-64): ', min_value=8, max_value=64)
                # Ask whether to include special characters
                include_special = prompt_yes_no('Include special characters?')
                try:
                    # Generate the password (may raise ValueError if invalid)
                    pw = generate_password(length, include_special)
                except Exception as e:
                    # Catch errors, show a message, and return to the menu
                    print('Error generating password:', e)
                    continue
                # Save the generated password to the file
                save_password(pw)
                # Display the password to the user
                print('\nGenerated password:')
                print(pw)
                # Inform where it was stored
                print(f'The password was appended to {PASSWORDS_FILE}.')

            # Option 2: Check password
            elif choice == '2':
                # Prompt the user to input the password and strip whitespace
                pw = input('Enter the password to check: ').strip()
                if not pw:  # Guard: reject empty input before evaluating strength
                    print('No password entered.')
                    continue
                # Determine strength and print result
                result = check_password_strength(pw)
                print(f'Strength: {result}')

            # Option 3: Quit (also accept common synonyms)
            elif choice == '3' or choice.lower() in ('q', 'quit', 'exit'):
                print('Exiting program.')
                break

            # Handle invalid choices
            else:
                print('Invalid selection — please choose 1, 2 or 3.')

    except (KeyboardInterrupt, EOFError):
        # Graceful exit on CTRL-C or EOF
        print('\nProgram terminated.')
    # Return code 0 signals successful exit
    return 0


if __name__ == '__main__':
    # When run as a script, execute main and exit with its return code.
    sys.exit(main())


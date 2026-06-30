# Password-Generator-and-Checker
A local Python console application to generate secure passwords, check password strength, and save the results to a text file.


---

## Features

- **Generate passwords** — create random passwords between 8 and 64 characters, with or without special characters
- **Check password strength** — evaluates any password as Weak, Medium, or Strong based on length and character variety
- **Save passwords** — all generated passwords are automatically saved to `data/passwords.txt`
- **Full input validation** — handles invalid types, out-of-range values, empty inputs, and unexpected exits gracefully

---

## How to Run

Make sure you have Python 3 installed, then run from the project root:

```bash
python3 src/main.py
```

---

## Menu Options

Generate a new password
Check a password
Quit


---

## Password Strength Criteria

| Rating | Length | Character Categories Required |
|--------|--------|-------------------------------|
| Strong | ≥ 12 characters | Uppercase, lowercase, digit, special character |
| Medium | ≥ 8 characters  | At least three of the four categories |
| Weak   | < 8 characters or fewer than three categories | — |

---

## Project Structure
Password-Generator-and-Checker/
├── src/
│   └── main.py          # All application source code
├── data/
│   └── passwords.txt    # Auto-created; stores generated passwords
├── tests/               # Test scripts
├── docs/                # Presentation and documentation
├── .gitignore
└── README.md

---

## Module Requirements Met

- ✅ Interactive app — console menu with continuous while-loop
- ✅ Data validation — type checking, range checking, empty input guard
- ✅ File processing — automatic directory creation, append mode, UTF-8 encoding

---

## Author

João-Manoel Roth — BSc Business Information Technology, FHNW

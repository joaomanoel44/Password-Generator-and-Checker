#!/usr/bin/env python3
import sys, os, string, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from main import generate_password, check_password_strength

PASS = "\033[92m✓ PASS\033[0m"
FAIL = "\033[91m✗ FAIL\033[0m"
results = []

def test(name, condition, detail=""):
    status = PASS if condition else FAIL
    print(f"  {status}  {name}" + (f"  [{detail}]" if detail else ""))
    results.append(condition)

print("=" * 60)
print("SECTION 1 — generate_password()")
print("=" * 60)

for l in [8, 10, 12, 16, 32, 64]:
    pw = generate_password(l, True)
    test(f"Exact length {l}", len(pw) == l, f"got {len(pw)}")

for _ in range(50):
    pw = generate_password(12, True)
test("Contains lowercase  (special=True)", any(c.islower() for c in pw))
test("Contains uppercase  (special=True)", any(c.isupper() for c in pw))
test("Contains digit      (special=True)", any(c.isdigit() for c in pw))
test("Contains special    (special=True)", any(c in string.punctuation for c in pw))

for _ in range(50):
    pw = generate_password(12, False)
test("No special chars    (special=False)", not any(c in string.punctuation for c in pw))

pw1 = generate_password(16, True)
pw2 = generate_password(16, True)
test("Passwords are randomised", pw1 != pw2)

try:
    pw = generate_password(8, True)
    test("Length=8 boundary allowed", len(pw) == 8)
except Exception as e:
    test("Length=8 boundary allowed", False, str(e))

try:
    generate_password(7, True)
    test("Length=7 raises ValueError", False)
except ValueError:
    test("Length=7 raises ValueError", True)

try:
    generate_password(0, False)
    test("Length=0 raises ValueError", False)
except ValueError:
    test("Length=0 raises ValueError", True)

try:
    generate_password(-5, False)
    test("Negative length raises ValueError", False)
except ValueError:
    test("Negative length raises ValueError", True)

print()
print("=" * 60)
print("SECTION 2 — check_password_strength()")
print("=" * 60)

for pw, label in [("Tr0ub4dor&3XX", "Strong – 14 chars"), ("Ab1!Ab1!Ab1!", "Strong – 12 chars")]:
    r = check_password_strength(pw)
    test(label, r == "Strong", f"got '{r}'")

for pw, label in [("Abcdef12", "Medium – upper+lower+digit"), ("abcdef1!", "Medium – lower+digit+special"), ("ABCDEF1!", "Medium – upper+digit+special")]:
    r = check_password_strength(pw)
    test(label, r == "Medium", f"got '{r}'")

for pw, label in [("password", "Weak – all lowercase"), ("12345678", "Weak – all digits"), ("!!!!!!!!!!", "Weak – all special"), ("AAAAAAAA", "Weak – all uppercase"), ("abc", "Weak – too short"), ("", "Weak – empty string")]:
    r = check_password_strength(pw)
    test(label, r == "Weak", f"got '{r}'")

test("Length 12 + 4 cats → Strong",  check_password_strength("Abcdef1234!@") == "Strong")
test("Length 11 + 4 cats → Medium",  check_password_strength("Abcdef123!@") == "Medium")
test("Length 8  + 3 cats → Medium",  check_password_strength("Abcdef12") == "Medium")
test("Length 7  + all cats → Weak",  check_password_strength("Abc1!Xy") == "Weak")

print()
print("=" * 60)
print("SECTION 3 — save_password() / file handling")
print("=" * 60)
import tempfile
import main as m

orig_data_dir = m.DATA_DIR
orig_pw_file  = m.PASSWORDS_FILE

with tempfile.TemporaryDirectory() as tmpdir:
    m.DATA_DIR       = os.path.join(tmpdir, "data")
    m.PASSWORDS_FILE = os.path.join(tmpdir, "data", "passwords.txt")
    pws = ["TestPass1!", "AnotherP@ss2", "Th1rd$ecret"]
    for pw in pws:
        m.save_password(pw)
    test("passwords.txt created automatically", os.path.isfile(m.PASSWORDS_FILE))
    with open(m.PASSWORDS_FILE, encoding="utf-8") as fh:
        lines = [l.rstrip('\n') for l in fh.readlines()]
    test("All 3 passwords written", lines == pws)
    m.save_password("FourthPw#9")
    with open(m.PASSWORDS_FILE, encoding="utf-8") as fh:
        lines2 = [l.rstrip('\n') for l in fh.readlines()]
    test("Append mode keeps previous entries", len(lines2) == 4)

m.DATA_DIR       = orig_data_dir
m.PASSWORDS_FILE = orig_pw_file

print()
print("=" * 60)
print("SECTION 4 — prompt_int() max_value validation")
print("=" * 60)
import builtins
from main import prompt_int

inputs = iter(["100", "64"])
original_input = builtins.input
builtins.input = lambda _: next(inputs)
output_msgs = []
original_print = builtins.print
builtins.print = lambda *a, **k: output_msgs.append(" ".join(str(x) for x in a))
result = prompt_int("test: ", min_value=8, max_value=64)
builtins.input = original_input
builtins.print = original_print
test("max_value=64 rejects 100", result == 64, f"got {result}")
test("Rejection message shown", any("at most 64" in msg for msg in output_msgs))

inputs2 = iter(["3", "8"])
builtins.input = lambda _: next(inputs2)
output_msgs2 = []
builtins.print = lambda *a, **k: output_msgs2.append(" ".join(str(x) for x in a))
result2 = prompt_int("test: ", min_value=8, max_value=64)
builtins.input = original_input
builtins.print = original_print
test("min_value=8 rejects 3", result2 == 8, f"got {result2}")

print()
print("=" * 60)
passed = sum(results)
total  = len(results)
colour = "\033[92m" if passed == total else "\033[93m"
print(f"{colour}RESULTS: {passed}/{total} tests passed\033[0m")
print("=" * 60)
sys.exit(0 if passed == total else 1)
PYEOF
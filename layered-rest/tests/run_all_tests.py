import subprocess
import sys

tests = [
    "test_add_remove.py",
    "test_vote.py",
    "test_sync.py",
    "test_metadata.py",
    "test_history.py"
]

all_passed = True
for test in tests:
    print(f"\nRunning {test}...")
    result = subprocess.run([sys.executable, test], cwd="./tests")
    if result.returncode != 0:
        print(f"{test}: FAIL")
        all_passed = False
    else:
        print(f"{test}: PASS")

if all_passed:
    print("\nALL TESTS PASSED")
else:
    print("\nSOME TESTS FAILED")

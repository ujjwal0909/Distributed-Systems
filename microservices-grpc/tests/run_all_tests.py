import os
import subprocess
import sys

def main():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [
        "test_add_remove.py",
        "test_vote.py",
        "test_sync.py",
        "test_metadata.py",
        "test_history.py",
    ]
    failures = 0
    for test in test_files:
        test_path = os.path.join(tests_dir, test)
        print(f"\nRunning {os.path.basename(test_path)}...")
        result = subprocess.run([sys.executable, test_path, "queue-service:50051"])
        if result.returncode != 0:
            print(f"{os.path.basename(test_path)}: FAIL")
            failures += 1
        else:
            print(f"{os.path.basename(test_path)}: PASS")
    if failures == 0:
        print("\nALL TESTS PASSED")
    else:
        print(f"\n{failures} TEST(S) FAILED")

if __name__ == "__main__":
    main()
import os
import subprocess
import sys

def main():
    # Get the absolute path to the tests directory (this file's directory)
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [
        "test_add_remove.py",
        "test_vote.py",
        "test_sync.py",
        "test_metadata.py",
        "test_history.py",
    ]
    all_passed = True
    for test in test_files:
        test_path = os.path.join(tests_dir, test)
        print(f"\nRunning {os.path.basename(test_path)}...")
        result = subprocess.run([sys.executable, test_path])
        if result.returncode != 0:
            print(f"{os.path.basename(test_path)}: FAIL")
            all_passed = False
        else:
            print(f"{os.path.basename(test_path)}: PASS")
    if all_passed:
        print("\nALL TESTS PASSED")
    else:
        print("\nSOME TESTS FAILED")

if __name__ == "__main__":
    main()

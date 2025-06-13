import csv
import subprocess
import sys

# === CONFIGURATION ===
STUDENT_SCRIPT = "FahrenheitToCelcius/Main.py"   # Name of student's script
CSV_FILE = "FahrenheitToCelcius/UnitTests/test_cases.csv"            # Your CSV file of test cases

def run_test_case(user_input, expected_output):
    try:
        result = subprocess.run(
            ["python3", STUDENT_SCRIPT],
            input=user_input,
            capture_output=True,
            text=True,
            timeout=5  # prevent infinite loops
        )

        # Clean up output for comparison
        actual_output = result.stdout.replace('\n', '').strip()
        expected_output = expected_output.replace('\n', '').strip()

        return actual_output == expected_output, actual_output

    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT]"

def run_all_tests():
    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        test_number = 1
        passed = 0
        total = 0

        for row in reader:
            total += 1
            user_input = row["input"].encode().decode("unicode_escape")  # decode \n
            expected_output = row["expected_output"].encode().decode("unicode_escape")

            passed_case, actual_output = run_test_case(user_input, expected_output)

            if passed_case:
                # print(f"✅ Test {test_number}: PASSED")
                passed += 1
            else:
                print(f"❌ Test {test_number}: FAILED")
                print(f"   Input: {repr(user_input)}")
                print(f"   Expected: {expected_output}")
                print(f"   Got     : {actual_output}")
            test_number += 1

        print(f"\n Summary: {passed}/{total} tests passed.")

if __name__ == "__main__":
    run_all_tests()

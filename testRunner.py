
import random
import time

import algorithms

# Skeleton test runner
# Can be modified to print out different outputs for our proposed tests
# Currently prints some generated tests for different sizes of n from a practice genetic sequence alphabet of 4 characters
# Output contains the runtime, and total operations for the Myers implementation and Dynamic programing implementation

# --------------------------------------------------
# Configuration
# --------------------------------------------------

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

ALPHABET = "ACGT"


# --------------------------------------------------
# Dataset Generation
# --------------------------------------------------

def generate_sequence(length, alphabet=ALPHABET):
    """Generate a random sequence of a specified length."""
    return "".join(random.choices(alphabet, k=length))


def generate_similar_pair(length, edit_percentage):
    """
    Generate two sequences that are mostly similar.

    edit_percentage controls approximately how many
    positions in B will differ from A.
    """
    seq_a = generate_sequence(length)
    seq_b = list(seq_a)

    num_changes = int(length * edit_percentage)

    positions = random.sample(
        range(length),
        min(num_changes, length)
    )

    for pos in positions:
        choices = [c for c in ALPHABET if c != seq_b[pos]]
        seq_b[pos] = random.choice(choices)

    return seq_a, "".join(seq_b)


def generate_test_cases():
    """Create test cases with different lengths and similarities."""

    test_cases = []

    lengths = [50, 100, 200, 400]
    similarities = [0.0, 0.10, 0.25, 0.50]

    for length in lengths:
        for edit_percentage in similarities:

            seq_a, seq_b = generate_similar_pair(
                length,
                edit_percentage
            )

            test_cases.append({
                "name": f"N={length}, changes={edit_percentage:.0%}",
                "seq_a": seq_a,
                "seq_b": seq_b
            })

    return test_cases


# --------------------------------------------------
# Script Validation
# --------------------------------------------------

def apply_script(seq_a, script):
    """
    Apply an edit script to A and return the resulting sequence.

    '=' : Keep character
    '-' : Delete character
    '+' : Insert character
    """

    result = []
    index_a = 0

    for operation, character in script:

        if operation == "=":
            if index_a >= len(seq_a) or seq_a[index_a] != character:
                raise ValueError("Invalid match operation")

            result.append(character)
            index_a += 1

        elif operation == "-":
            if index_a >= len(seq_a) or seq_a[index_a] != character:
                raise ValueError("Invalid deletion operation")

            index_a += 1

        elif operation == "+":
            result.append(character)

        else:
            raise ValueError(f"Unknown operation: {operation}")

    if index_a != len(seq_a):
        raise ValueError("Script did not consume all of sequence A")

    return "".join(result)


# --------------------------------------------------
# Benchmarking
# --------------------------------------------------

def benchmark_dp(seq_a, seq_b):
    algorithms.reset_ops()

    start = time.perf_counter()

    distance = algorithms.dp_len(seq_a, seq_b)

    elapsed = time.perf_counter() - start

    operations = algorithms.ops["dp_cells"]

    return distance, operations, elapsed


def benchmark_myers(seq_a, seq_b):
    algorithms.reset_ops()

    start = time.perf_counter()

    distance, script = algorithms.myers_len(seq_a, seq_b)

    elapsed = time.perf_counter() - start

    operations = algorithms.ops["myers_steps"]

    return distance, script, operations, elapsed


# --------------------------------------------------
# Test Runner
# --------------------------------------------------

def run_tests():

    test_cases = generate_test_cases()

    print("\nINSERTION-DELETION EDIT DISTANCE")
    print("=" * 100)

    print(
        f"{'Test Case':<25}"
        f"{'Distance':>10}"
        f"{'DP Ops':>15}"
        f"{'Myers Ops':>15}"
        f"{'DP Time(ms)':>15}"
        f"{'Myers Time(ms)':>18}"
        f"{'Correct':>10}"
    )

    print("-" * 100)

    results = []

    for case in test_cases:

        seq_a = case["seq_a"]
        seq_b = case["seq_b"]

        # Run DP
        dp_distance, dp_ops, dp_time = benchmark_dp(
            seq_a, seq_b
        )

        # Run Myers
        myers_distance, script, myers_ops, myers_time = (
            benchmark_myers(seq_a, seq_b)
        )

        # Verify distances
        correct_distance = dp_distance == myers_distance

        # Verify edit script
        try:
            transformed = apply_script(seq_a, script)
            valid_script = transformed == seq_b
        except ValueError:
            valid_script = False

        correct = correct_distance and valid_script

        results.append({
            "name": case["name"],
            "distance": dp_distance,
            "dp_ops": dp_ops,
            "myers_ops": myers_ops,
            "dp_time": dp_time,
            "myers_time": myers_time,
            "correct": correct
        })

        print(
            f"{case['name']:<25}"
            f"{dp_distance:>10}"
            f"{dp_ops:>15,}"
            f"{myers_ops:>15,}"
            f"{dp_time * 1000:>15.4f}"
            f"{myers_time * 1000:>18.4f}"
            f"{str(correct):>10}"
        )

    print("=" * 100)

    # Summary
    successful = sum(r["correct"] for r in results)

    print(f"\nTests passed: {successful}/{len(results)}")

    return results


if __name__ == "__main__":
    results = run_tests()

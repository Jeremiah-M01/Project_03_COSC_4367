import itertools 
import random 


from algorithms import (dp_len, dp_script, myers_len, myers_script, ops, reset_ops)

# The worked example from the paper (Figure 1), also traced in Section 3 of our presentation.
PAPER_A = "abcabba"
PAPER_B = "cbabac"

def brute_force_d(a, b):
    """Try every subsequence of a, longest first, until one is also in b."""
    def in_b(sub):
        it = iter(b)
        return all(s in it for s in sub)
    for size in range(len(a), -1, -1):
        for picks in itertools.combinations(a, size):
            if in_b(picks):
                return len(a) + len(b) - 2 * size


def apply_script(seq_a, script):
    """Run an edit script on seq_a and return what it builds.
    Fails if a kept or deleted symbol is not the next one in seq_a."""
    built = []
    pos_a = 0
    for op, symbol in script:
        if op == "+":
            built.append(symbol)
            continue
        assert pos_a < len(seq_a) and seq_a[pos_a] == symbol, f"script does not match A at {pos_a}"
        if op == "=":
            built.append(symbol)
        pos_a += 1
    assert pos_a == len(seq_a), "script left part of A unread"
    return built


def check_script(seq_a, seq_b, d, script):
    """A valid script turns A into B and spends exactly D edits."""
    assert apply_script(seq_a, script) == list(seq_b)
    assert sum(1 for op, _ in script if op != "=") == d


def kept(script):
    """The matched symbols of a script, which spell out its LCS."""
    return "".join(symbol for op, symbol in script if op == "=")


def test_paper_example():
    """abcabba -> cbabac: D = 5 with an LCS of length 4."""
    assert brute_force_d(PAPER_A, PAPER_B) == 5
    assert dp_len(PAPER_A, PAPER_B) == 5
    assert myers_len(PAPER_A, PAPER_B) == 5
    for d, script in (dp_script(PAPER_A, PAPER_B), myers_script(PAPER_A, PAPER_B)):
        assert d == 5
        check_script(PAPER_A, PAPER_B, d, script)
        assert len(kept(script)) == 4
    # Several LCSs tie at length 4. DP's walk back finds cbba; the greedy path
    # finds caba, the one in Figure 1 of the paper.
    assert kept(myers_script(PAPER_A, PAPER_B)[1]) == "caba"


def test_paper_example_edit_script():
    """The walk back from (7,6) gives the edits in Figure 1: 1D, 2D, 3IB, 6D, 7IC."""
    _, script = myers_script(PAPER_A, PAPER_B)
    assert script == [("-", "a"), ("-", "b"), ("=", "c"), ("+", "b"), ("=", "a"),
                      ("=", "b"), ("-", "b"), ("=", "a"), ("+", "c")]


def test_paper_example_work():
    """Greedy: 19 lane updates + 11 snake steps = 30. DP fills all 7 x 6 inner cells = 42."""
    reset_ops()
    myers_len(PAPER_A, PAPER_B)
    assert ops["myers_steps"] == 30
    reset_ops()
    myers_script(PAPER_A, PAPER_B)
    assert ops["myers_steps"] == 30
    reset_ops()
    dp_len(PAPER_A, PAPER_B)
    assert ops["dp_cells"] == 42


def test_edge_cases():
    cases = [("", ""), ("", "abc"), ("abc", ""), ("abc", "abc"), ("aaa", "bbb"), ("a", "b")]
    for a, b in cases:
        expected = brute_force_d(a, b)
        assert dp_len(a, b) == expected
        assert myers_len(a, b) == expected
        for d, script in (dp_script(a, b), myers_script(a, b)):
            assert d == expected
            check_script(a, b, d, script)


def test_random_against_brute_force():
    """All four agree with brute force on small inputs, over a 2- and a 4-letter alphabet."""
    rng = random.Random(4367)
    for trial in range(600):
        alphabet = "ab" if trial % 2 else "abcd"
        a = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
        b = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
        expected = brute_force_d(a, b)
        assert dp_len(a, b) == expected, (a, b)
        assert myers_len(a, b) == expected, (a, b)
        for d, script in (dp_script(a, b), myers_script(a, b)):
            assert d == expected, (a, b)
            check_script(a, b, d, script)


def test_myers_len_matches_script_on_larger_inputs():
    """Too big for brute force, so check Myers against DP instead."""
    rng = random.Random(7)
    for _ in range(50):
        a = [rng.randint(0, 9) for _ in range(rng.randint(50, 120))]
        b = list(a)
        for _ in range(rng.randint(0, 15)):  # a few random edits keeps D small
            if b and rng.random() < 0.5:
                del b[rng.randrange(len(b))]
            else:
                b.insert(rng.randint(0, len(b)), rng.randint(0, 9))
        expected = dp_len(a, b)
        assert myers_len(a, b) == expected
        d, script = myers_script(a, b)
        assert d == expected
        check_script(a, b, d, script)


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print("passed", test.__name__)
    print(f"all {len(tests)} tests passed")

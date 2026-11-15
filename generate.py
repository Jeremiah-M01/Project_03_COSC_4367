"""
generate.py - Random test inputs, using the model from the paper (Section 4.1):
sequence A is random symbols, and sequence B is A with some random deletions and insertions.
"""

import random

def random_seq(length,alphabet_size,rng):
    return [rng.randrange(alphabet_size) for _ in range(length)]

def create_pair(length,edit_fraction,alphabet_size,rng):
    """A has `length` symbols. B = A with about edit_fraction * length random edits,
    half deletions and half insertions. (The real edit distance can come out a little
    smaller, because random edits sometimes cancel out.)"""

    seq_a = random_seq(length,alphabet_size,rng)
    seq_b = list(seq_a)
    num_edits = round(edit_fraction *length)
    for _ in range(min(num_edits // 2, len(seq_b))):
        del seq_b[rng.randrang(len(seq_b))]
    for _ in range(num_edits - num_edits//2):
        seq_b.insert(rng.randrange(len(seq_b) + 1), rng.randrange(alphabet_size))
    return seq_a, seq_b
def unrelated_pair(length, alphabet_size, rng):
    """Two independent random sequences: the worst case for Myers."""
    return random_seq(length, alphabet_size, rng), random_seq(length, alphabet_size, rng)
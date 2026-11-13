import itertools 
import random 


from algorithms import (dp_len, dp_script, myers_len)#still need to add 

def brute_force_d(a, b):
    """Try every subsequence of a, longest first, until one is also in b."""
    def in_b(sub):
        it = iter(b)
        return all(s in it for s in sub)
    for size in range(len(a), -1, -1):
        for picks in itertools.combinations(a, size):
            if in_b(picks):
                return len(a) + len(b) - 2 * size
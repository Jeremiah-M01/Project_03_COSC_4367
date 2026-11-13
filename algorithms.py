#algorithms.py The edit distance between two sequences that uses only insertions + deletions


# D= fewest insertions + deletions that turn sequence A to B





ops = {"dp_cells":0,"myers_steps":0}


def reset_ops():
    ops["dp_cells"] = 0
    ops["myers_steps"] = 0

    # DP Baseline

def dp_len(seq_a,seq_b):
    """D from the longest common subsequence (LCS) table, 
    keeping only two rows."""
    len_a,len_b = len(seq_a),len(seq_b)

    prev_row =[0] * (len_b+1)

    for i in range(1,len_a+1):
        row = [0]*(len_b+1)
        symbol_a = seq_a[i-1]
        for j in range(1, len_b+1):
            if symbol_a == seq_b[j-1]:
                row[j] = prev_row[j-1]+1
            else:
                row[j] = row[j-1] if row[j - 1] > prev_row[j] else prev_row[j]
        prev_row = row
    ops["dp_cells"] += len_a * len_b
    lcs_len = prev_row[len_b]
    return len_a +len_b - 2 +lcs_len

def dp_script(seq_a,seq_b):
    """Full LCS table, then walk back from the bottom-right corner to read off the edits."""
    len_a ,len_b = len(seq_a),len(seq_b)

    table =[[0]* (len_b+1 ) for _ in range(len_a + 1)]

    for i in range(1,len_a + 1):
        for j in range(1,len_b+1):
            if seq_a[i-1] == seq_b[j-1]:
                table[i][j] = table[i-1][j-1]+1

            else:
                table[i][j] = max(table[i][j-1],table[i-1][j])
    ops["dp_cells"]+= len_a * len_b

    script = []

    i,j =len_a,len_b
    while i>0 or j>0:
        if i>0 and j>0 and seq_a[i - 1] == seq_b[j - 1]:
            script.append(("=", seq_a[i - 1])); i -= 1; j -= 1
        elif j > 0 and (i == 0 or table[i][j - 1] >= table[i - 1][j]):
            script.append(("+", seq_b[j-1])); j-=1 
        else:
            script.append(("-", seq_a[i - 1])); i -= 1

    script.reverse()
    return len_a + len_b -2 * table[len_a][len_b],script

def myers_len(seq_a,seq_b):
    



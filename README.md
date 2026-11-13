# Project_03_COSC_4367
We are going to implement and test the paper's claims against the straightforward DP solution. Myers solves the shortest edit script problem in a greedily in a O((N+M)D) time, claims O(N+M+D²)
expected time, and offers a linear space variant, but acknowledges that it loses when D is large. We will implement his basic and linear space algorithms alongside the classic O(NM)  dynamic programming solution then compare their run-times on both generated and real world file inputs. The end goal is to identify the conditions under which Myers algorithm is faster, and the point at which differences grow large enough for DP to overtake it.


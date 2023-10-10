from __future__ import annotations
from typing import List

from libs.kmap import Minterms, Term


def extract(regno: str) -> List[int]:
    nums: List[int] = []
    for i in regno:
        if i.isnumeric():
            nums.append(int(i))
        elif 'A' <= i <= 'F':
            nums.append(int(i, 16))

    return list(set(nums))


def notop(F: List[int]) -> List[int]:
    return [i for i in range(16) if i not in F]


def get_eqns(f_vals: List[int], inverted: bool = False):
    f_vals = notop(f_vals) if inverted else f_vals
    min_terms: List[str] = [Term("%04d" % int(bin(i)[2:])) for i in f_vals]
    mask = Minterms(min_terms).simplify()
    eqns = []

    # Make into ~ABCD form
    for term in mask:
        eqns.append(''.join([("~" if term.term[i] == '0' else "") + chr(ord("A")+i) for i in range(len(term.term)) if term.term[i] != "*"]))

    return eqns

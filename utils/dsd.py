from __future__ import annotations
from typing import List

from libs.kmap import Minterms, Term


def extract(regno: str) -> List[int]:
    nums: List[int] = []
    for i in regno:
        if 'A' <= i <= 'F' or i.isnumeric():
            nums.append(int(i, 16))

    return list(set(nums))


def extract_in_order(regno: str) -> List[int]:
    nums: List[int] = []
    for i in regno:
        if 'A' <= i <= 'F' or i.isnumeric():
            if int(i, 16) in nums:
                continue
            nums.append(int(i, 16))

    return nums


def notop(F: List[int]) -> List[int]:
    return [i for i in range(16) if i not in F]


def get_eqns(f_vals: List[int], inverted: bool = False, pos: bool = False):
    f_vals = notop(f_vals) if inverted else f_vals
    min_terms: List[str] = [Term("%04d" % int(bin(i)[2:])) for i in f_vals]
    mask = Minterms(min_terms).simplify()
    eqns = []

    # Make into ~ABCD form
    for term in mask:
        string = ""
        for i in range(len(term.term)):
            if term.term[i] != "*":
                not_sym = ("~" if ((term.term[i] == '0') ^ (pos)) else "")
                string += not_sym + chr(ord("A")+i)
        eqns.append(string)

    return eqns

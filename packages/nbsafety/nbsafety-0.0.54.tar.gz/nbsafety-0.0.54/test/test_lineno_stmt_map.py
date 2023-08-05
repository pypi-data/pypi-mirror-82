# -*- coding: utf-8 -*-
import ast

from nbsafety.analysis.lineno_stmt_map import compute_lineno_to_stmt_mapping


def test_for_loop():
    code = """
for i in range(10):
    a: int = i
    b = a + i
    lst: List[int] = [a, b]
""".strip()
    mapping = compute_lineno_to_stmt_mapping(code)
    assert isinstance(mapping[1], ast.For)
    assert isinstance(mapping[2], ast.AnnAssign)
    assert isinstance(mapping[3], ast.Assign)
    assert isinstance(mapping[4], ast.AnnAssign)


def test_multiline_for_loop():
    code = """
for i in [
    0,
    1,
    2,
    3,
    4,
]:
    a = i
    b = a + i
    lst = [a, b]
""".strip()
    mapping = compute_lineno_to_stmt_mapping(code)
    for i in range(1, 7):
        assert isinstance(mapping[i], ast.For)
    assert 7 not in mapping
    assert isinstance(mapping[8], ast.Assign)
    assert isinstance(mapping[9], ast.Assign)
    assert isinstance(mapping[10], ast.Assign)

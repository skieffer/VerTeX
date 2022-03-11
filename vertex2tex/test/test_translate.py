# VerTeX | Copyright (c) 2010-2022 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

import pytest

from vertex2tex.v2t import *
from vertex2tex.document import translate_document

from vertex2tex.test.test_tokenize import text1, translated1

def test_translate_1():
    t = translate_snippet(text1)
    print(t)
    assert t == translated1

text2 = [
    "$alp$",
    "$@alp$",
    "$alp@$",
    "$@alp@$",
    "$$alp$$",
    "$$@alp$$",
    "$$alp@$$",
    "$$@alp@$$",
]

out2 = [
    "$alp$",
    r"$\alpha$",
    r"$\alpha$",
    r"$\alpha$",
    "$$alp$$",
    r"$$\alpha$$",
    r"$$\alpha$$",
    r"$$\alpha$$",
]

def test_translate_2():
    """
    Test that, with the default keychar of "@", translate_document maps vertex to tex
    iff the keychar appears first, or last, or both.
    """
    for t, expected in zip(text2, out2):
        out = translate_document(t)
        print(out)
        assert out == expected


@pytest.mark.parametrize('raw, expected', [
    ['a1, a2, ddd, an+1', 'a_{1}, a_{2},\\ldots, a_{n+1}'],
    ['xivv1, xivv2, ddd, xivvm', 'x_{i_{1}}, x_{i_{2}},\\ldots, x_{i_{ m}}'],
    ['aijuu2', 'a_{i j}^{2}'],

    ['pi', 'p_{i}'],
    ['alphan', '\\alpha_{n}'],
    ['bbZm', '\\mathbb{Z}_{m}'],
    ['cn+1', 'c_{n+1}'],
    ['ai,j', 'a_{i, j}'],
    ['zeta', '\\zeta'],

    ['auur', 'a^{ r}'],
    ['a^^r', 'a^{ r}'],

    ['aiuur', 'a_{i}^{ r}'],
    ['ai^^r', 'a_{i}^{ r}'],

    ['auurvvk', 'a^{ r_{ k}}'],
    ['a^^r__k', 'a^{ r_{ k}}'],
    # Can mix with ordinary TeX:
    ['a^{rk}', 'a^{ r_{k}}'],
    ['a^{r_k}', 'a^{ r_ k}'],

    ['aivvj', 'a_{i_{ j}}'],
    ['ai__j', 'a_{i_{ j}}'],

    ['aivvjuur', 'a_{i_{ j}^{ r}}'],
    ['ai__j^^r', 'a_{i_{ j}^{ r}}'],

    ['aivvjUUr', 'a_{i_{ j}}^{ r}'],
    ['ai__j^^^r', 'a_{i_{ j}}^{ r}'],

    ['zvveta', r'z_{\eta}'],
    ['z__eta', r'z_{\eta}'],
    ['z_eta', r'z_\eta'],
])
def test_translate_3(raw, expected):
    assert translate_snippet(raw) == expected


@pytest.mark.parametrize('raw, expected', [
    ['a0, a1, ddd, an-1', 'a_{0}, a_{1},\\ldots, a_{n-1}'],
    ['alpha, beta, gamma', '\\alpha,\\beta,\\gamma'],
    ['frp in bbZ', '\\mathfrak{p}\\in\\mathbb{Z}'],
    ['n eth', 'n^{\\mathrm{th}}'],
    ['frac 2 over 3;', '\\frac{2}{3}'],
    ['abs x', '\\left| x\\right|'],
    ['f supp n', 'f^{( n)}'],
    ['f inv', 'f^{-1}'],
    ['sum over n from 0 to infty; an', '\\sum_{ n=0}^{\\infty} a_{n}'],

    ['f squ', 'f^2'],
    ['alp', '\\alpha'],
    ['lam', '\\lambda'],
    ['Lam', '\\Lambda'],
    ['vep', '\\varepsilon'],
    ['vph', '\\varphi'],
    ['pie', '\\pi'],
    ['frp sfM bfv bbQ calO scrB', '\\mathfrak{p}\\mathsf{M}\\mathbf{v}\\mathbb{Q}\\mathcal{O}\\mathscr{B}'],
])
def test_translate_4(raw, expected):
    assert translate_snippet(raw) == expected


@pytest.mark.parametrize('raw, expected', [
    ['foo', 'f_{o o}'],
    [r'\\foo', 'foo'],
    [r'\\', r'\\'],
    [r'\foo', r'\foo'],
])
def test_translate_5(raw, expected):
    assert translate_snippet(raw) == expected


if __name__ == "__main__":
    test_translate_1()

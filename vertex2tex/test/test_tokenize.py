# VerTeX | Copyright (c) 2010-2022 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

from vertex2tex.v2t import *

text1="""
abs
    matrix 4 cols
        1; 1; 1; 1;
        1; zeta; zeta^^2r; zeta^^2r-1;
        1; (zeta) squ; (zetauu2r) squ; (zetauu2r-1) squ;
        1; (zeta)^3; (zetauu2r)^3; (zetauu2r-1)^3;
    endmatrix
;
equiv 0 mod frl^ell
"""

translated1 = (
    r"\left|\begin{array}{cccc}1&1&1&1\\"
    r"1&\zeta&\zeta^{2 r}&\zeta^{2 r-1}\\"
    r"1&(\zeta)^2&(\zeta^{2 r})^2&(\zeta^{2 r-1})^2\\"
    r"1&(\zeta)^3&(\zeta^{2 r})^3&(\zeta^{2 r-1})^3\\"
    r"\end{array}\right|\equiv0~\mathrm{mod}~\mathfrak{l}^\ell"
)

tokens1 = ['\n', 'abs', '\n    ', 'matrix', ' ', '4', ' ', 'cols', '\n        ', '1',
           ';', ' ', '1', ';', ' ', '1', ';', ' ', '1', ';', '\n        ', '1', ';',
           ' ', 'zeta', ';', ' ', 'zeta^^2r', ';', ' ', 'zeta^^2r-1', ';', '\n        ',
           '1', ';', ' ', '(', 'zeta', ')', ' ', 'squ', ';', ' ', '(', 'zetauu2r', ')',
           ' ', 'squ', ';', ' ', '(', 'zetauu2r-1', ')', ' ', 'squ', ';', '\n        ',
           '1', ';', ' ', '(', 'zeta', ')', '^', '3', ';', ' ', '(', 'zetauu2r', ')',
           '^', '3', ';', ' ', '(', 'zetauu2r-1', ')', '^', '3', ';', '\n    ',
           'endmatrix', '\n', ';', '\n', 'equiv', ' ', '0', ' ', 'mod', ' ', 'frl', '^',
           'ell', '\n'
]

def test_tokenize_1():
    tokens = tokenize(text1)
    print()
    print(tokens)
    assert tokens == tokens1


if __name__ == "__main__":
    test_tokenize_1()

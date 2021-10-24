# VerTeX | Copyright (c) 2010-2021 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

from vertex2tex.v2t import *
from vertex2tex.document import translate_document

from vertex2tex.test.test_tokenize import text1

def test_translate_1():
    t = translate_snippet(text1)
    print(t)

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

if __name__ == "__main__":
    test_translate_2()

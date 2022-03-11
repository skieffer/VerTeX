# VerTeX | Copyright (c) 2010-2022 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

from vertex2tex.v2t import *

in1 = "a   b   '   '   c"
out1 = "a b'' c"

def test_compress_1():
    assert compress(in1) == out1


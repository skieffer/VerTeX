# VerTeX | Copyright (c) 2010-2022 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

"""
Processing whole documents.
"""

import re

from vertex2tex.excep import *
from vertex2tex.v2t import translate_snippet

class Segment:
    """
    Represents the segments into which the input text is broken in the lexing process.

    A Segment holds the text of the segment, along with the
    line and column numbers at which the text began in the
    original document, and along with a tag giving the type of the
    segment, which is either 'text' or 'bdry' (boundary).
    """

    # Segment types:
    TEXT = "text"
    BDRY = "bdry"

    def __init__(self, L, C, T, S):
        self.line = L
        self.column = C
        self.type = T
        self.string = S

    def getLine(self): return self.line

    def getCol(self): return self.column

    def getType(self): return self.type

    def getStr(self): return self.string

    def getLCTS(self):
        L = self.line; C = self.column; T = self.type
        S = self.string
        return (L,C,T,S)

    def __str__(self, w=3):
        # if you want the line and column numbers to be
        # formatted to be width at least W, then set
        # the keyword argument w = W.
        t = '%%%sd, %%%sd, %%s: '%(w, w)
        L = self.line; C = self.column; T = self.type
        s = t % (L,C,T)
        s += repr(self.string)
        return s

class SegmentStream:
    """
    SegmentStream lexes a given document into alternating
    text and boundary segments, and then serves as a stream from
    which the segments can be requested, one after another.
    """

    def __init__(self, text):
        self.text = text
        #You pass the text to be parsed.
        bd = re.compile( # 'bd' is for 'boundary'
            r'((?<!\\)\$\$|(?<!\\)\$|'+ # $$ or $ (but not when escaped)
            r'(?<!\\)\\\[|(?<!\\)\\\])' # \[ or \]
        )
        self.segs = bd.split(text)
        self.reset()

    def reset(self):
        # Line and column numbers will be 1-based, as in most popular text editors.
        self.line = 1
        self.column = 1
        self.nexttype = Segment.TEXT
        self.ptr = 0

    def getTextPos(self):
        return (self.line, self.column)

    def next(self):
        # If there are no segments left, return 'None'
        if self.ptr >= len(self.segs): return None
        # Get next type and segment.
        nt = self.nexttype
        ns = self.segs[self.ptr]
        # Build Segment object
        seg = Segment(self.line, self.column, nt, ns)
        # Advance type and pointer
        self.nexttype = Segment.BDRY if nt == Segment.TEXT else Segment.TEXT
        self.ptr += 1
        # Update line and column numbers
        lines = ns.split('\n')
        y = len(lines)-1
        if y > 0:
            self.line += y
            self.column = len(lines[-1])
        else:
            self.column += len(ns)
        # Return the Segment
        return seg

def translate_document(text, keychar="@"):
    r"""
    Process an entire document, translating from VerTeX to TeX, discovering math modes, and optionally
    checking for a keychar.

    NB: Nested math modes are not handled!
        We only handle $...$, $$...$$, and \[...\] math modes, with no others nested inside them.

    :param text: The text to be processed.
    :param keychar: Must be either None or a single character (but not $ or \).
                    Pass None if you want VerTeX to be applied to all text occurring within math modes.
                    Otherwise VerTeX is applied only when the text within the math mode
                    begins or ends with the keychar (or both).
    :return: The text of the translated document.
    """
    if keychar is not None:
        assert len(keychar) == 1
        assert keychar not in r'\$'
    segs = SegmentStream(text)
    out = ''
    n = 0
    seg = segs.next()
    while seg:
        t = seg.getStr()
        # Math mode contents occur precisely on the segments of index 2 mod 4.
        if n == 2 and t:
            try:
                if keychar is None:
                    t = translate_snippet(t)
                else:
                    i0 = 1 if t[0] == keychar else 0
                    i1 = 1 if t[-1] == keychar else 0
                    if i0 + i1:
                        t = translate_snippet(t[i0:len(t)-i1])
            except VerTeXError as ve:
                # Note the segment where the error occurred, and re-raise.
                ve.set_segment(seg)
                raise ve
        out += t
        # Increment n mod 4, and get next segment.
        n = (n + 1) % 4
        seg = segs.next()
    return out

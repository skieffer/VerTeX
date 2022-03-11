# VerTeX | Copyright (c) 2010-2022 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

class VerTeXError(Exception):

    def __init__(self, msg):
        self.msg = msg
        self.segment = None

    def set_segment(self, seg):
        self.segment = seg

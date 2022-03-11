# VerTeX | Copyright (c) 2010-2022 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

"""
Translating math mode snippets from VerTeX to TeX.
"""

import re

from vertex2tex.config import *


###############
# Node classes

class Node:
    """
    The basic Node class, which contains the basic translation method (`xlat`).

    Other node types should subclass Node and simply override the three methods `buildArg`,
    `addcomma`, and `build`, as needed.
    """

    def __init__(self, token_stream):
        self.toks = token_stream
        self.output = ''
        # Subclasses should override self.commawords, if necessary.
        self.commawords = []  # Basic Node considers nothing to be a commaword.

    ###########################################################
    # If possible, subclasses should use 'Node's basic xlat
    # method below, and customize it simply by overriding
    # the following three methods.

    def buildArg(self, s):
        self.output += s+' '

    def addcomma(self, T):
        """
        Should return True iff it is time to quit (i.e. the final comma word has been received).
        """
        self.buildArg(T)
        return False

    def build(self):
        return self.output.strip()

    ###########################################################

    def xlat(self):
        T = self.toks.next()
        while T:
            # First check if the token is escaped with a \.
            if T[0] == '\\':
                # Tokens beginning with double backslash and having at least one character beyond
                # that are passed through after lopping off the backslashes.
                if len(T) >= 3 and T[1] == '\\':
                    s = T[2:]
                # Otherwise, the token passes through unaltered. So this includes both the case of a token
                # that begins only with a single backslash, and the case of a double backslash followed
                # by nothing else, as is used in TeX arrays, for example.
                else:
                    s = T
                self.buildArg(s)

            # Let HTML codes like &gt; and &lt; pass through unaltered.
            elif T in html_exceptions:
                s = T
                self.buildArg(s)

            elif T in unarynodes:
                code = unarynodes[T]
                lefty = UnaryNode(code, self.toks)
                s = lefty.xlat()
                self.buildArg(s)

            elif T in binarynodes:
                w, c, o = binarynodes[T]
                lefty = BinaryNode(w, c, o, self.toks)
                s = lefty.xlat()
                self.buildArg(s)

            elif T in tertiarynodes:
                w, c, o = tertiarynodes[T]
                lefty = TertiaryNode(w, c, o, self.toks)
                s = lefty.xlat()
                self.buildArg(s)

            elif T in rangenodes:
                symbol = rangenodes[T]
                lefty = RangeNode(symbol,self.toks)
                s = lefty.xlat()
                self.buildArg(s)

            elif T in specialnodes:
                klass = specialnodes[T]
                lefty = klass(self.toks)
                s = lefty.xlat()
                self.buildArg(s)

            elif T in self.commawords:
                tobreak = self.addcomma(T)
                if tobreak: break

            elif T in builtins:
                s = builtins[T]
                self.buildArg(s)

            elif T in bsmes:
                self.buildArg('\\'+T)

            elif fontword(T):
                s = fontword(T)
                self.buildArg(s)

            #Automatic subscripting
            elif (len(T) >= 2 and
                  re.match('[A-Za-z]', T) and
                  T.find(' ') == -1):
                s = autosub(T)
                self.buildArg(s)

            #Anything else just passes through.
            else:
                self.buildArg(T)

            #Get the next token.
            T = self.toks.next()

        s = self.build()
        return s


class UnaryNode(Node):

    def __init__(self, wrappers, ts):
        self.toks = ts
        self.wrappers = wrappers
        self.stuff = ''
        self.commawords = [';']

    def buildArg(self, s):
        self.stuff += s+' '

    def addcomma(self, T):
        return True

    def build(self):
        a = self.stuff
        w = self.wrappers
        s = w[0]+a+w[1]
        return s

class BinaryNode(Node):

    def __init__(self, wrappers, comma, order, ts):
        self.toks = ts
        self.wrappers = wrappers
        self.commawords = [comma,';']
        self.order = order
        self.args = ['','']
        self.argptr = 0

    def buildArg(self, s):
        self.args[self.argptr] += s+' '

    def addcomma(self, T):
        self.argptr += 1
        return T == ';'

    def build(self):
        a, b = [self.args[i] for i in self.order]
        w = self.wrappers
        s = w[0]+a+w[1]+b+w[2]
        return s

class TertiaryNode(Node):

    def __init__(self, wrappers, comma, order, ts):
        self.toks = ts
        self.wrappers = wrappers
        self.commawords = list(comma)+[';']
        self.order = order
        self.args = ['','','']
        self.argptr = 0
        self.commaseq = []

    def buildArg(self, s):
        self.args[self.argptr] += s+' '

    def addcomma(self, T):
        self.argptr += 1
        self.commaseq.append(T)
        return T == ';'

    def build(self):
        a, b, c = [self.args[i] for i in self.order]
        w = self.wrappers
        s = w[0]+a+w[1]+b+w[2]+c+w[3]
        return s

class RangeNode(Node):

    def __init__(self, symbol, ts):
        self.toks = ts
        self.symbol = symbol
        self.commawords = ['over', 'from', 'to', ';']
        self.args = ['', '', '']
        self.argptr = -1
        self.commaseq = []

    def buildArg(self, s):
        self.args[self.argptr] += s+' '

    def addcomma(self, T):
        self.argptr += 1
        self.commaseq.append(T)
        return T == ';'

    def build(self):
        if self.commaseq == [';']:
            s = self.symbol+' '
        elif self.commaseq == ['over', ';']:
            c = self.symbol
            r = self.args[0]
            s = c+'_{'+r+'} '
        elif self.commaseq == ['over', 'from', 'to', ';']:
            c = self.symbol
            v, a, b = self.args
            s = c+'_{'+v+'='+a+'}^{'+b+'} '
        else:
            s = '--error in range operator--'
        return s

class Matrixnode(Node):
    """
    To make a matrix of N columns (we don't care how
    many rows you make), start with the keyword
    'matrix', then write out the number N, then the
    keyword 'cols', and then write the entries, separated
    by semicolons. You don't have to start a new line; we
    handle that automatically based on the number of columns.

    Thus, you can't start a new line early; we need to see
    N semicolons in order to complete each line.

    When you've written the last entry, you should not follow
    it by a semicolon. Just write the keyword 'endmatrix'.
    (A semicolon will cause a new row to begin, giving you
     one blank row at the end of your matrix.)
    """

    def __init__(self, ts):
        self.toks = ts
        self.commawords = ['cols', ';', 'endmatrix']
        self.args = []
        self.stuff = ''
        self.cols = 0
        self.err = False

    def buildArg(self, s):
        self.stuff += s+' '

    def addcomma(self, c):
        if c == 'endmatrix':
            if self.stuff: self.args.append(self.stuff)
            done = True
        elif c == 'cols':
            try: self.cols = int(self.stuff)
            except: self.err = True
            self.stuff = ''
            done = False
        else: # c == ';'
            self.args.append(self.stuff)
            self.stuff = ''
            done = False
        return done

    def build(self):
        if self.err: s = '-- error in matrix node --'
        else:
            C = self.cols
            s = '\\begin{array}{'
            s += 'c'*C
            s += '}'
            A = self.args
            for k in range(len(A)):
                r = k%C
                if r > 0: s += ' & '
                s += A[k]
                if r == C-1: s += '\\\\'
            if s[-1] != '\n': s += '\n'
            s += '\\end{array}'
        return s


class Padspnode(Node):
    """
    This is intended for p-adic numbers with extra spaces
    between the digits. Probably you can think of other uses
    for it too.

    The name could mean 'p-adic space node' or 'padded space node'.

    When you've written the last entry, you can follow
    it by a semicolon, but you don't have to. To end,
    write the keyword 'end'.
    """

    def __init__(self, ts):
        self.toks = ts
        self.commawords = [';', 'end']
        self.args = []
        self.stuff = ''
        self.spacer = '\\: '
        self.err = False

    def buildArg(self, s):
        self.stuff += s+' '

    def addcomma(self, c):
        if c == 'end':
            if self.stuff: self.args.append(self.stuff)
            done = True
        else: # c == ';'
            self.args.append(self.stuff)
            self.stuff = ''
            done = False
        return done

    def build(self):
        if self.err: s = '-- error in padsp node --'
        else:
            s = self.spacer.join(self.args)
        return s

specialnodes = {
    'matrix': Matrixnode,
    'padsp': Padspnode
}

##########
# Auto-subscripting

# Regular expressions to match letter sets and variations:

any_letter = all_letter_re_component+"|[A-Za-z]"
letter_matcher = re.compile(any_letter)

opt_font_any_letter = '(%s)?(%s)' % (
    font_prefix_re_component, any_letter
)
letter_matcher_fonts = re.compile(opt_font_any_letter)

r = '(%s|[0-9,+-])' % opt_font_any_letter
sub_matcher = re.compile(r)

r = r'(UU|uu|vv|\^\^\^|\^\^|__|%s|[0-9,+-])' % opt_font_any_letter
uusub_matcher = re.compile(r)


def autosub(s):
    r"""
    Autosubscripting (and superscripting).

    If s is a string starting with some [A-Za-z], and having no
    spaces in it, and has already failed
    to match anything else (so, it was not escaped with a \, it
    was not a leftword, commaword, userdef, built-in def, bsme word,
    or font-letter), then we do automatic subscripting.

    First we match the longest letter name we can, at the beginning
    of s. Call this L, and call the remainder R. We then split R
    into letter names, digits, and the characters [+-,], translate
    this as needed, and put them all together into a subscript.

    The exceptions are the codes 'uu' and 'vv'. If we find 'uu'
    anywhere in the subscript, this switches us from subscript to
    superscript. You may use 'uu' without any foregoing subscript.

    The code 'vv' initiates a subscript. If used in the midst of
    another subscript, you will get a double subscript, as in
    $a_{i_1}$. If used in the midst of a superscript, you will get a
    subscript on the superscript, as in $2^{alpha_i}$. If used as
    the very first thing in an automatic subscript, it will have no
    effect, but is useful in creating a subscript which would
    otherwise have triggered a keyword. For example, 'pvvie' will
    give $p_{i e}$ instead of $\pi$.
    """
    #Make sure s starts with a letter, and has no spaces.
    #If it is not so, then return the empty string.
    if not re.match('[A-Za-z]', s) or s.find(' ') >= 0: return ''

    #translator class
    class Xlator:

        def __init__(self):
            self.vvcount = 0
            self.state = 0

        def reset(self):
            self.vvcount = 0; self.state = 0

        def xlat(self,t):
            s = ''

            if t in ['uu', '^^']: s = '}^{'
            elif t in ['UU', '^^^']:
                if self.vvcount == 0:
                    s = t
                else:
                    self.vvcount -= 1
                    s = '}}^{'
            elif t in ['vv', '__']:
                # If 'vv' is the very first token, do not raise vvcount.
                if self.state > 0: self.vvcount += 1
                s = '_{'
            else: s = Node(TokenStream([t])).xlat()

            if self.state == 0: self.state = 1
            return s

        def getvvcount(self):
            return self.vvcount

    #create translator instance
    X = Xlator()

    #Match the longest initial vertex letter.
    M = letter_matcher_fonts.match(s)
    L = X.xlat(M.group())
    s = s[M.end():]

    #Parse and translate the subscript.
    X.reset()
    A = uusub_matcher.findall(s)
    sub = ' '.join([X.xlat(x[0]) for x in A])
    sub = '_{'+sub+'}'
    sub += '}'*X.getvvcount()
    if sub[:3] == '_{}': sub = sub[3:] # in case started with uu
    elif sub[:3] == '_{_': sub = sub[2:] # in case started with vv

    return L+sub

##########

def fontword(T):
    """
    Check whether T is of the form <font><letter>.
    If so, return the string that should be passed to
    the parsing node's buildArg method. If not, return
    an empty string.
    """
    #translation function
    def xlat(t):
        return Node(TokenStream([t])).xlat()

    s = ''
    if len(T) > 0 and letter_matcher.split(T)[-1] == '':
        letter = letter_matcher.findall(T)[-1]
        prefix = T[:-len(letter)]
        if prefix in fonts:
            font = fonts[prefix]
            letter = xlat(letter)
            s = '\\%s{%s}'%(font,letter)
    return s

class TokenStream:

    def __init__(self,token_list):
        self.token_list = token_list
        self.k = 0
        self.N = len(token_list)

    def next(self):
        """
        Return the next token, or None if none remain.
        """
        if self.k < self.N:
            T = self.token_list[self.k]
            self.k += 1
            return T
        else:
            return None

    def showRest(self):
        """
        Return a list containing a copy of the remaining
        tokens.
        """
        return self.token_list[self.k:]

    def getPtr(self):
        """
        Get the current pointer value.
        """
        return self.k

    def getSlice(self,a,b):
        """
        Return the tokens in the clopen interval from a to b.
        Thus, you get token a, but not b.
        In other words, it's just the [a:b] slice.
        """
        return self.token_list[a:b]



TOKEN_RE = re.compile(
    (r'\\{' +
     r'|\\[^{\s]*' +
     r'|[A-Za-z](?:[A-Za-z0-9+\-,]|\^\^\^|\^\^|__)*[A-Za-z0-9]' +
     r'|#\d+' +
    "|"+"|".join(html_exceptions) +
     r'|\S' +
     r'|\s+')
)

def tokenize(text):
    return re.findall(TOKEN_RE, text)

def compress(text):
    """
    Delete all whitespace characters except those followed by an upper or lowercase letter.
    :param text: The text to be compressed.
    :return: The compressed text.
    """
    return re.sub(r'\s+(?![a-zA-Z])', '', text)

def translate_snippet(text):
    """
    Translate a single "snippet" (i.e. the contents of a TeX math mode) from VerTeX into plain TeX.
    :param text: The text of the snippet.
    :return: The translated text.
    """
    tokens = tokenize(text)
    ts = TokenStream(tokens)
    root = Node(ts)
    out = root.xlat()
    out = compress(out)
    return out

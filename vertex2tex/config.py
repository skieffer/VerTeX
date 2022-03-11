# VerTeX | Copyright (c) 2010-2022 Steve Kieffer | MIT license
# SPDX-License-Identifier: MIT

# Built-ins (special abbreviations)
builtins = {
    # Dots
    'ccc':'\\cdots', 'ddd':'\\ldots', 'vvv':'\\vdots',
    # Arrows
    'to':'\\rightarrow',
    'gets':'\\leftarrow',
    'implies':'\\Rightarrow',
    # Infixes
    'equ':'=', 'div':'|',
    'plus':'+', 'minus':'-',
    'in':'\\in',
    'ltn':'<', 'gtn':'>',
    # Differential operators
    'par':'\\partial', 'grad':'\\nabla',
    # mod
    'mod':'~\\mathrm{mod}~',
    # Signs
    'mipl':'\\mp', 'plmi':'\\pm',
    # The best empty set :)
    'empty':'\\varnothing',

    # Common superscripts
    # (1) Powers
    'inv':'^{-1}', 'squ':'^2', 'cubed':'^3',
    # (2) Ordinals
    'rst':'^{\\mathrm{st}}',
    'ond':'^{\\mathrm{nd}}',
    'ird':'^{\\mathrm{rd}}',
    'eth':'^{\\mathrm{th}}',
    # (3) Other
    'star':'^*', 'mult':'^\\times', 'deg':'^\\circ',
}

# Three-letter names for every Greek letter:
Greek_three_letter = {
    # (1) Those whose names are ordinarily longer than three letters:
    # (1a) Lowercase:
    'alp':'\\alpha', 'bet':'\\beta', 'gam':'\\gamma',
    'del':'\\delta', 'eps':'\\epsilon', 'zet':'\\zeta',
    'the':'\\theta', 'iot':'\\iota', 'kap':'\\kappa',
    'lam':'\\lambda', 'sig':'\\sigma', 'ups':'\\upsilon', 'ome':'\\omega',
    # (1b) Uppercase, where different from Roman letters:
    'Gam':'\\Gamma', 'Del':'\\Delta', 'The':'\\Theta',
    'Lam':'\\Lambda', 'Sig':'\\Sigma', 'Ome':'\\Omega',
    # (2) Those whose names are ordinarily shorter than three letters:
    # (2a) Lowercase:
    'mew':'\\mu', 'new':'\\nu', 'pie':'\\pi', 'ksi':'\\xi',
    # (2b) Uppercase, where different from Roman letters:
    'Pie':'\\Pi', 'Ksi':'\\Xi',
    # (3) Variants
    'vep':'\\varepsilon', 'vph':'\\varphi',
    'vth':'\\vartheta', 'vpi':'\\varpi',
}

# Add these to the built-ins.
builtins.update(Greek_three_letter)

# Backslash-me's; same as an existing LaTeX code; we just add the
# leading backslash for you.
bsmes = [
    'mapsto', 'leq', 'geq', 'neq', 'times',
    'subseteq', 'supseteq', 'subsetneq', 'supsetneq',
    'subset', 'supset',
    'wedge', 'vee', 'not', 'cdot',
    'top', 'bot',
    'det',
    'equiv', 'cong', 'sim',
    'cup', 'cap', 'setminus',
    'nmid', 'mid',
    'infty',
    'ker',
    'iff', 'forall', 'exists',
    'int', 'sin', 'cos', 'log', 'exp',
    'tan', 'arctan', 'arcsin', 'arccos',
    'quad', 'qquad',
]

bsme_letters = [
    'ell',
    # We include all Greek letters. (So you don't have to use the three-letter
    # built-in abbreviations if you don't want to.)
    'alpha', 'beta', 'gamma', 'delta', 'epsilon',
    'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda',
    'rho', 'sigma', 'tau', 'upsilon',
    'phi', 'chi', 'psi', 'omega',
    'Gamma', 'Delta', 'Theta', 'Lambda', 'Sigma',
    'Phi', 'Psi', 'Omega'
]

# Include the letters.
bsmes.extend(bsme_letters)

# We'll need one giant list of all things that can count as letter names.
all_letter_names = bsme_letters + list(Greek_three_letter.keys())
# And we will use this to build regexes.
all_letter_re_component = "|".join(all_letter_names)

# Font and decorator prefixes.
fonts = {
    'fr':'mathfrak',
    'sf':'mathsf',
    'bf':'mathbf',
    'bb':'mathbb',
    'rm':'mathrm',
    'cal':'mathcal',
    'scr':'mathscr',
    'bar':'bar',
    'hat':'hat',
    'til':'tilde'
}

font_prefixes = fonts.keys()
font_prefix_re_component = "|".join(font_prefixes)

unarynodes = {
    'of':('(',')'),
    'qnt':('\\left( ', '\\right)'), # quantity
    'bqnt':('\\left[', '\\right]'), # bracket quantity
    'set':('\\left\\lbrace ', ' \\right\\rbrace'),
    'abs':('\\left|', '\\right|'),
    'seq':('\\left\\langle', '\\right\\rangle'),
    'floor':('\\left\\lfloor', '\\right\\rfloor'),
    'ceil':('\\left\\lceil', '\\right\\rceil'),
    'sup':('^{','}'),
    'supp':('^{(',')}'),
    'sub':('_{','}'),
    'pmod':('~\\left(\\mathrm{mod}\\, ', '\\right)'), # (mod _)
    'sqrt':('\\sqrt{', '}'),
    'bar':('\\bar{', '}'),
    'tilde':('\\tilde{', '}'),
    'hat':('\\hat{', '}'),
    'widehat':('\\widehat{', '}'),
    'words':('\\:\\mbox{', '}\\:') #plain text words in math mode
}

binarynodes = {
    # fraction
    'frac':[ ('\\frac{', '}{', '}'), 'over', [0, 1] ],
    # nth root:
    'root':[ ('\\sqrt[', ']{', '}'), 'base', [0, 1] ],
    # Legendre symbol:
    'legen':[ ('\\left(\\frac{', '}{', '}\\right)'), 'over', [0, 1] ],
    # binomial coefficient
    'binom':[ ('\\binom{', '}{', '}'), 'choose', [0, 1] ],
    # index (of a subgroup), or degree of a field extension
    'index':[ ('\\left[', ' : ', '\\right]'), 'in', [1, 0] ]
}

tertiarynodes = {
    'map':[ ('', ' : ', '\\rightarrow', ''), ('from', 'to'), [0, 1, 2] ]
}

rangenodes = {
    'sum':'\\sum', 'product':'\\prod', 'prod':'\\prod',
    'limit':'\\lim',
    'union':'\\bigcup', 'inters':'\\bigcap'
}

html_exceptions = [
    '&gt;',
    '&lt;',
    '&apos;',
    '&quot;',
    '&amp;'
]

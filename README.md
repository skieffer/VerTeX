# VerTeX: Verbal TeX

Do you find anything cumbersome about TeX syntax? For example, 

| If instead of this...       | you'd prefer to type this...   |
|:----------------------------|:-------------------------------|
| a_0, a_1, \ldots, a_{n-1}   | a0, a1, ddd, an-1              |
| \alpha, \beta, \gamma, ...  | alpha, beta, gamma, ...        |
| \mathfrak{p} \in \mathbb{Z} | frp in bbZ                     |
| n^\mathrm{th}               | n eth                          |
| \frac{2}{3}                 | frac 2 over 3;                 |
| \left\| x \right\|          | abs x;                         |
| f^{(n)}                     | f supp n;                      |
| f^{-1}                      | f inv                          |
| \sum_{n=0}^\infty a_n       | sum over n from 0 to infty; an |

...then VerTeX may be for you!

VerTeX is pronounced "ver-tech," and stands for "Verbal TeX," i.e. TeX
in which what you type is often much closer to what you _say_ when you read
mathematics aloud.

I developed VerTeX while I was translating German mathematics into English,
and I wanted to be able to type symbolic expressions as quickly as I could
type words.

Therefore one of the goals of VerTeX is to help you keep your
fingers over the home row. This leads to some verbal equivalents that may
appeal to some, but not to others.

However, another feature of VerTeX is that -- with a few key exceptions
(see below) -- ordinary TeX syntax passes through unaltered, so that you may
use as many or as few of the features of VerTeX as you wish.

# Usage

There are just two main functions that you'll make use of:
`translate_snippet`, and `translate_document`.

Apply `translate_snippet` directly to math mode contents written in VerTeX,
in order to translate them into plain TeX:

    >>> from vertex2tex import *
    >>> translate_snippet('bbQ(alp)')
    '\\mathbb{Q}(\\alpha)'

When working on an entire document, use `translate_document`.
The default behavior of `translate_document` is to translate
the contents of math modes _only if they begin or end (or both) with a `@` character
inside the usual dollar sign delimiters_.
(The `@` char(s) are then omitted from the output.)
This allows you to be selective about where VerTeX is used, and where it isn't.

In particular, this means you can begin typing your math mode expressions as usual, and
only when you're done decide if you used any VerTeX or not. If so, include a `@` before
the final `$` or `$$`. If not, leave it out. Thus

    >>> translate_document('$alp@$')
    '$\\alpha$'

but

    >>> translate_document('$alp$')
    '$alp$'

Alternatively, this behavior can be modified by using the `translate_document` function's
keyword argument `keychar`. Setting `keychar=None` means that VerTeX translation will be
applied to _all_ text occurring within math modes:

    >>> translate_document('$alp$', keychar=None)
    '$\\alpha$'


# The VerTeX Language

## Slash the Backslashes!

When you are writing mathematics, how often do you want a Greek letter alpha, and how
often do you want to multiply the variables a, l, p, h, and a together, in that
order? Why then should `$alpha$` give you a sequence of Roman letters, while
the Greek letter requires a backslash?

In VerTeX, `$alpha$` yields the Greek letter, and if you really want the product of variables,
simply put spaces between the letters, as in `$a l p h a$`.

In general, VerTeX keywords are not strings of letters preceded by a backslash,
but simply strings of letters uninterrupted by whitespace.
Conceptually, the keywords in VerTeX may be divided into the following four
kinds, according to the role they play in avoiding backslashes.

Types of VerTeX keywords:

1. bsme
2. built-in
3. bracket word
4. font prefix

If you want to see (and perhaps alter locally) the lists of keywords, just
consult the `config.py` module in the `vertex` package.

### bsmes

"bsme" stands for "backslash me," and a bsme keyword is
one that is exactly the same as a keyword in TeX, except without the backslash.
It produces the exact same result as the corresponding TeX keyword.
For the list of all bsme keywords, consult the `config.py` module.

### built-ins

The so-called “built-in” keywords do not correspond to any existing TeX keywords.
They do not take any arguments, but simply translate directly into some
string of TeX, and their purpose is to in one way or another give an easier way
to type certain commonly used TeX strings.

In particular, one of the goals of VerTeX is to give you the option to keep
your fingers over the home row while typing, and for this reason the built-in
keywords provide many alphabetical equivalents to TeX strings that ordinarily
involve non-alphabetical characters. For example, `inv` (for “inverse”) produces
`^{-1}`, and `squ` (for “squared”) produces `^2`.

For the list of all built-ins, consult the `config.py` module.

#### Going Greek

Greek letters are near and dear to our heart in mathematics. They should
be easy to type.
In VerTeX, _every_ Greek letter -- including the variants -- has a
_three-letter name_. And yes, this even includes the letters whose names
are ordinarily only two-letters long, like pi and mu!

For example, you may type `alp` for alpha, `lam` for lambda, or
`Lam` for capital Lambda.

You may type `vep` for `varepsilon` (everybody's favorite epsilon),
and `vph` for `varphi`.

As for pi, xi, mu, and nu, these letters have funny three-letter spellings
(anyone for `pie`?) in order to get around the auto-subscripting mechanism
discussed below.

As usual, consult `config.py` for the full lists.

You do not have to use these abbreviations if you don't want to.
Every Greek letter whose name is ordinarily _more_ than two letters long
is also a `bsme` keyword, so just go right ahead and spell it out if you
want to, whether it's `alpha`, `lambda`, or `Omega`.

### bracket words

In TeX there are many constructions in which a keyword takes arguments
surrounded by braces `{ }`. For example,

    \frac{\pi}{4}
    
yields the sum of the Bhaskara-Leibniz Series. In VerTex, the same
construction is achieved by

    frac pie over 4;
    
In this example, `frac`, `over`, and the final semicolon `;` serve as
_bracket words_.

In general, when a construction takes arguments, then the arguments
are to be surrounded by the appropriate bracket words. For the most part, the
final bracket word will be a semicolon.

The list of all such constructions in VerTeX can be found in `config.py`,
under the `unarynodes`, `binarynodes`, `tertiarynodes`, and `rangenodes`
definitions. It includes many popular constructions, such as
sets, sequences, floors, ceilings, absolute values, "mod" expressions,
Legendre symbols, binomial coefficients, sums, products, and more.

### font (and decorator) prefixes

Technically font prefixes are not “keywords” in and of themselves. They are
two- or three-character prefixes which, when followed by a letter of the alphabet,
produce that letter in the appropriate font. The prefixes and the fonts that they
correspond to can be found in `config.py`.

For example, instead of

    \mathfrak{p} \mathsf{M} \mathbf{v} \mathbb{Q} \mathcal{O} \mathscr{B}

you may type

    frp sfM bfv bbQ calO scrB
    
to achieve the same thing.

You can also use prefixes to get things like hats and tildes. For example,
instead of `\hat{x}` just type `hatx`.



## Auto-Subscripts (and Superscripts)

In mathematics, subscripted variables are the coin of the realm, and therefore it
ought to be easy to type them. VerTeX makes it fast and easy to get subscripts
and superscripts. For example,

| Cumbersome TeX...                   | ...is easy in VerTeX       |
|:------------------------------------|:---------------------------|
| `a_1, a_2, \ldots, a_{n+1}`         | `a1, a2, ddd, an+1`        |
| `x_{i_1}, x_{i_2}, \ldots, x_{i_m}` | `xivv1, xivv2, ddd, xivvm` |
| `a_{i j}^2`                         | `aijuu2`                   | 

The _semiautomatic subscripting and superscripting_ (henceforth SSS) mechanism of
VerTeX is very handy, and, as the examples in the table show, makes it
much easier to type certain common kinds of subscripts and superscripts.

While many subscript and superscript combinations can be achieved through
SSS, some things are not possible. In such cases, you can use the `sub` and `sup`
bracket words, or can even fall back on standard TeX syntax.

The complete description of the SSS process is a bit complex, but for most
common purposes it is quite simple. Therefore before we give a detailed
specification of the process, we consider the main ideas.

First we need some terminology. We all know what subscripts and superscripts
are, but what do we call the letter they get attached to? Let's call it the "base".

**In most cases, the process is simple**: VerTeX will take a word `w` and split it as
`w = bs`, where `b` is the longest initial segment of `w` that matches as a letter
name, and `s` is everything that remains. Then `b` will be the base, and `s`
will be the subscript.

Examples (and one non-example):

| VerTeX | TeX          |
|:-------|:-------------|
| pi     | p_i          |
| alphan | \alpha_n     |
| bbZm   | \mathbb{Z}_m |
| cn+1   | c_{n+1}      |
| ai,j   | a_{i,j}      |
| zeta   | \zeta        |

There are several things to note about these examples:

1. It was so that `pi` could be available for automatic subscripting that we gave
the Greek letter pi the (admittedly somewhat silly) spelling `pie`. Writing `p_i`
is a perhaps daily occurrence for anyone who works with prime numbers, and
this includes a lot of mathematicians.

2. Letters with extended names, like `alpha`, and letters with a font prefix in
front of them, like `bbZ`, _will_ indeed be counted as initial letters.

3. Commas, as well as plus and minus signs, are considered part of the word.

4. What happened with `zeta`? Perhaps we were hoping this would translate
to `z_\eta`, but of course VerTeX instead matched the entire word zeta as the base.
There is a way to get around this, which we discuss below. Preview: You may type
`zvveta` in order to get `z_\eta`.

#### The Details

To the VerTeX parser, a "word" consists of alphanumeric characters, as well
as commas and the plus and minus symbols. It must begin with an alphabetical
character. (In other words a “letter,” but this means one of the ASCII letters in
the character class `[A-Za-z]`, and is not to be confused with all things
that may be considered "letters" in VerTeX, which includes, for example,
Greek letters, and letters with font prefixes.)

For those familiar with regular expressions, this means that words
are built on the character class
    
    [A-Za-z0-9+-,]

The last three symbols are included in the character class because they are
common in subscripts.
(**However**, this means that if you do not want to accidentally trigger a subscript,
you need to put whitespace on at least one side of these characters!)

Now suppose that `w` is the next word that VerTeX has to process. If `w` fails
to match as any kind of
keyword – bsme, built-in, bracket word, or font-prefix-letter combination -- then `w` is
submitted to the SSS process.

VerTeX first matches the longest possible letter name at the beginning of `w`,
as discussed above. Let the word `w` consist of initial letter `b` followed by
remainder `s`, that is, `w = bs`. Then `b` will be the base, and `s` will give one or
more subscripts and/or superscripts.

In the simplest case, `s` simply represents a subscript. It is possible however to
switch between subscripts and superscripts using the special character sequences
`vv`, `uu`, and `UU`.

NEW in Version 0.3.3: As alternatives to the character sequences
`vv`, `uu`, and `UU`, you may also use, respectively,
`__`, `^^`, and `^^^`.

A few examples illustrate all the ways to use these control sequences:

| VerTeX   | TeX       |
|:---------|:----------|
| auur     | a^r       |
| aiuur    | a_i^r     |
| auurvvk  | a^{r_k}   |
| aivvj    | a_{i_j}   |
| aivvjuur | a_{i^r_j} |
| aivvjUUr | a_{i_j}^r |
| zvveta   | z_\eta    |

The rules are:

* Sequence `vv` opens a deeper subscript. In TeX it is as though you typed `_{`.
* Sequence `uu` closes a subscript and opens a superscript. In TeX it is as
  though you typed `}^{`.
* Seuqnece `UU` closes _two_ subscripts and opens a superscript. In TeX it is as
  though you typed `}}^{`.
* One special exception is that if `vv` is used at the very beginning of `s`,
  it merely keeps you at the first subscript level. Thus, `zvveta` provides a way
  to produce `z_\eta`, while `zeta` simply gives `\zeta`.

Again, use of these special control sequences may appeal to some, but not to
others. They facilitate fast typing, but are perhaps not as good when it comes
time to _read_ the code later. Of course, you can still use the
ordinary `^` and `_` of TeX if you prefer.


## Use only what you want

VerTeX is 99% transparent to ordinary TeX.
That means you can type (almost) any ordinary TeX you want, and it will pass
through the VerTeX filter unaltered. So, use as many or as few of the features
of VerTex as you wish.

#### What are the gotchas?

The main gotchas are keywords and automatic subscripting; but the solution
is always very simple: Add spaces!

If a sequence of characters has been matched as a VerTeX keyword but this
is not what you wanted, just put one or more spaces between those characters.

Likewise, if automatic subscripting is taking place when you don't want it,
the solution is the same: separate the characters with spaces.

#### Safety net

As a “safety net,” any word whatsoever may be prefixed with a double
backslash `\\` in order to allow that word to pass through VerTeX unaltered.
To be precise, if there is any remainder `w` to the word, then this, minus the two
backslashes, is what will pass through. If just two backslashes alone are typed,
they will pass though unaltered (which is useful in TeX table environments).
Meanwhile, any word beginning with a single backslash is passed through VerTeX
completely unaltered, i.e. with the leading backslash still intact.
In summary:

    \\w  -->  w
    \\   -->  \\
    \w   -->  \w

where `w` is a word at least one character long.

But you probably won't need to use this anyway. In using VerTeX for ten years,
I cannot recall needing it once.

Enjoy!

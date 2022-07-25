
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'

import sys
import optparse
import textwrap

from lib.slimit import mangler
from lib.slimit.parser import Parser
from lib.slimit.visitors.minvisitor import ECMAMinifier


def minify(text, mangle=False, mangle_toplevel=False):
    parser = Parser()
    tree = parser.parse(text)
    if mangle:
        mangler.mangle(tree, toplevel=mangle_toplevel)
    minified = ECMAMinifier().visit(tree)
    return minified


def main(argv=None, inp=sys.stdin, out=sys.stdout):
    usage = textwrap.dedent("""\
    %prog [options] [input file]

    If no input file is provided STDIN is used by default.
    Minified JavaScript code is printed to STDOUT.
    """)
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-m', '--mangle', action='store_true',
                      dest='mangle', default=False, help='mangle names')
    parser.add_option('-t', '--mangle-toplevel', action='store_true',
                      dest='mangle_toplevel', default=False,
                      help='mangle top level scope (defaults to False)')

    if argv is None:
        argv = sys.argv[1:]
    options, args = parser.parse_args(argv)

    if len(args) == 1:
        text = open(args[0]).read()
    else:
        text = inp.read()

    minified = minify(
        text, mangle=options.mangle, mangle_toplevel=options.mangle_toplevel)
    out.write(minified)

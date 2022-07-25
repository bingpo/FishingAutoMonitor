
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'

from lib.slimit.scope import SymbolTable
from lib.slimit.visitors.scopevisitor import (
    ScopeTreeVisitor,
    fill_scope_references,
    mangle_scope_tree,
    NameManglerVisitor,
    )


def mangle(tree, toplevel=False):
    """Mangle names.

    Args:
        toplevel: defaults to False. Defines if global
        scope should be mangled or not.
    """
    sym_table = SymbolTable()
    visitor = ScopeTreeVisitor(sym_table)
    visitor.visit(tree)

    fill_scope_references(tree)
    mangle_scope_tree(sym_table.globals, toplevel)

    mangler = NameManglerVisitor()
    mangler.visit(tree)

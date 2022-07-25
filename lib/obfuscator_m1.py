#!/usr/bin/python3
import random
from lib.slimit import ast
from lib.slimit import minify
from lib.slimit.parser import Parser
from lib.slimit.visitors import nodevisitor

import lib.obfuscator_mi_lib.boolean_obfuscator as boolean_obfuscator
import lib.obfuscator_mi_lib.number_obfuscator as number_obfuscator
import lib.obfuscator_mi_lib.string_obfuscator as string_obfuscator


def level_1(src):
    parser = Parser()
    tree = parser.parse(src)
    for node in nodevisitor.visit(tree):
        #: Obfuscate all constants
        if isinstance(node, ast.Boolean):
            node.value = str(boolean_obfuscator.make_expression(node.value.lower() == 'true', random.randint(5, 20)))
        if isinstance(node, ast.Number):
            node.value = str(number_obfuscator.make_expression(int(node.value), random.randint(5, 8)))
        if isinstance(node, ast.String):
            node.value = string_obfuscator.obfuscate_string(str(node.value[1:-1]))
    return tree.to_ecma()  # print awesome javascript :)


def obfuscate_js_m1(src):
    """ Goes through every level of obfuscation """
    src = level_1(src)
    src = minify(src, mangle=True)
    return src


if __name__ == "__main__":
    js_code = "alert(1)"

    print(obfuscate_js_m1(js_code))

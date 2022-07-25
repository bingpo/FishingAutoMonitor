import random

hex_chars = [chr(i) for i in range(97, 103)]
hex_number = [chr(i) for i in range(49, 58)]


def randomComplexHex():
    return '0x' + random.choice(hex_chars) + str(random.randint(10, 15))


def randomHHex():
    return '0x' + random.choice(hex_number) + random.choice(hex_number) + random.choice(hex_number)


def randomHex():
    return '0x' + random.choice(hex_number) + random.choice(hex_number)


def charToExp(letter):
    exp = randomComplexHex() + '+-' + randomHHex() + '+' + randomHex() + '*' + randomHex() + '-' + randomHex() + '*0x' + random.choice(hex_number)
    return exp + '+-' + str(hex(eval(exp) - ord(letter)))


def sentToExp(string):
    return ','.join(charToExp(i) for i in string)


def codeToExp(code):
    return 'window["\\x65\\x76\\x61\\x6C"](window["\\x65\\x76\\x61\\x6C"]("\\x74\\x68\\x69\\x73\\x5b\\x22\\x53\\x74\\x72\\x69\\x6e\\x67\\x22\\x5d\\x5b\\x22\x66\\x72\\x6f\\x6d\\x43\\x68\\x61\\x72\\x43\\x6f\\x64\\x65\\x22\\x5d")(' + sentToExp(
        code) + '))'


def ezObfuscate(code):
    return "window['\\x65\x76\\x61\\x6C']('{}')".format("".join("\\x{:02x}".format(ord(c)) for c in code))


def obfuscate_js_m2(code):
    return codeToExp(ezObfuscate(code))


def de_obfuscate(code):
    code = code.replace(
        'window["\\x65\\x76\\x61\\x6C"](window["\\x65\\x76\\x61\\x6C"]("\\x74\\x68\\x69\\x73\\x5b\\x22\\x53\\x74\\x72\\x69\\x6e\\x67\\x22\\x5d\\x5b\\x22\x66\\x72\\x6f\\x6d\\x43\\x68\\x61\\x72\\x43\\x6f\\x64\\x65\\x22\\x5d")',
        'eval(String.fromCharCode')
    code = code.replace('eval(String.fromCharCode(', '');
    code = code.replace('))', '')
    res = ''
    split = code.split(',')
    for i in range(len(split)):
        res += chr(eval(split[i]))
    return eval(res.replace("window['\\x65v\\x61\\x6C'](", '').replace(')', ''))


if __name__ == "__main__":
    js_code = "alert(1)"
    print(obfuscate_js_m2(js_code))

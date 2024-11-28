from functools import reduce

def strip_whitespace(str):
    return " ".join(str.split())


def replace(str, replacements):
    return reduce(lambda a, kv: a.replace(*kv), replacements, str)


def clean(str):
    replacements = [("[new page]", "")]
    return replace(strip_whitespace(str), replacements)


def load_text(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read()
    return data


def snippet(str, left, right):
    start = str.find(left)
    end = str.find(right) + len(right)
    return str[start:end]


def include(target_str, passages):
    return " ".join(map(lambda tup: snippet(target_str, tup[0], tup[1]), passages))


def get_text(filename, including):
    return (include(clean(load_text(filename)), including))

def process(filename, including):
    text = get_text(filename, including)
    return get_adjectives(text)
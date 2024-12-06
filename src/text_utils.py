from functools import reduce

def strip_whitespace(input_str: str) -> str:
    """Removes excess whitespace."""
    return " ".join(input_str.split())


def replace_string(input_str: str, replacements: list[tuple[str, str]]) -> str:
    """Replaces substrings."""
    return reduce(lambda s, kv: s.replace(*kv), replacements, input_str)


def clean_text(input_str: str) -> str:
    """Cleans text by removing whitespace and specified substrings."""
    replacements = [("[new page]", "")]
    return replace_string(strip_whitespace(input_str), replacements)


def load_text(filename: str) -> str:
    """Loads text from file."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def extract_snippet(input_str: str, left_marker: str, right_marker: str) -> str:
    """Extracts snippet between markers."""
    start = input_str.find(left_marker)
    end = input_str.find(right_marker) + len(right_marker)
    return input_str[start:end]


def combine_snippets(input_str: str, passages: list[tuple[str, str]]) -> str:
    """Combines snippets."""
    return " ".join(map(lambda tup: extract_snippet(input_str, *tup), passages))


def get_text(filename: str, markers: list[tuple[str, str]]) -> str:
    """Extracts relevant text from file."""
    text = load_text(filename)
    cleaned_text = clean_text(text)
    return combine_snippets(cleaned_text, markers)
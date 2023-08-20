import re

__version__ = "0.1.3"


def regex_to_int(c):
    return int(c, 16)

def regex_to_chr(c):
    return chr(regex_to_int(c))


def regex_unicode_char_literal(ch):
    escaped = re.escape(ch)
    if escaped != ch:
        return escaped

    return ch.encode('unicode_escape').decode()

def regex_chars_to_ranges(chars, sorted=False):
    char_set = set()
    unique_chars = []
    for c in chars:
        if c not in char_set:
            unique_chars.append(c)
            char_set.add(c)

    if not sorted:
        unique_chars.sort(key=regex_to_int)

    char_ranges = []
    prev = None
    start_range = None
    end_range = None
    n = len(unique_chars)
    for i, c in enumerate(unique_chars):
        current = regex_to_int(c)

        if prev is not None and prev == current - 1:
            if start_range is None:
                start_range = regex_unicode_char_literal(chr(prev))
            end_range = regex_unicode_char_literal(chr(current))
            if i == n - 1:
                char_ranges.append('-'.join([start_range, end_range]))
                start_range = None
                end_range = None
        else:
            if start_range is not None and end_range is not None:
                char_ranges.append('-'.join([start_range, end_range]))
            elif prev:
                char_ranges.append(regex_unicode_char_literal(chr(prev)))

            if i < n - 1:
                start_range = regex_unicode_char_literal(chr(current))
                end_range = None
            else:
                char_ranges.append(regex_unicode_char_literal(chr(current)))
        prev = current
    return char_ranges

def regex_char_range(match):
    r = match.split("..")
    # Wide version
    return "-".join(
        [
            regex_unicode_char_literal(regex_to_chr(c))
            for c in r
        ]
    )


def regex_multi_chars(match):
    r = match.split(" ")
    return "".join([
        "".join(
        [
            regex_unicode_char_literal(regex_to_chr(c))
            for c in r
        ]),
    ])



def regex_char_patterns(text, *regexes):
    char_patterns = []
    for line in text.split("\n"):
        for regex in regexes:
            m = regex.match(line)
            if not m:
                continue
            chars = m.group(1).strip()
            if " " not in chars:
                char_patterns.append(regex_char_range(chars))
            else:
                char_patterns.append(regex_multi_chars(chars))
    return char_patterns

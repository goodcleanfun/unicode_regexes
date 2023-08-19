import re

__version__ = "0.1.2"


def regex_to_int(c):
    return int(c, 16)

def regex_to_chr(c):
    return chr(regex_to_int(c))

def regex_unicode_char_literal(c):
    ch = regex_to_chr(c)
    escaped = re.escape(ch)
    if escaped != ch:
        return escaped

    return (
        "\\u{}".format(c.lower())
        if len(c) < 5
        else "\\U{}".format(c.lower().rjust(8, "0"))
    )

def regex_char_range(match):
    r = match.split("..")
    # Wide version
    return "-".join(
        [
            regex_unicode_char_literal(c)
            for c in r
        ]
    )


def regex_multi_chars(match):
    r = match.split(" ")
    return "".join([
        "".join(
        [
            regex_unicode_char_literal(c)
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

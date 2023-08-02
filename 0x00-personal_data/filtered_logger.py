#!/usr/bin/env python3
"""ALX SE Regex-ing"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns an obfuscated log message passed in message"""
    for pattern in fields:
        regex_pattern = r'({}=).*?({})'.format(pattern, separator)
        message = re.sub(regex_pattern, r'\1{}\2'.format(redaction), message)
    return message

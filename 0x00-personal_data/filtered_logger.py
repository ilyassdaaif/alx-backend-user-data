#!/usr/bin/env python3
"""Module for obfuscating sensitive information in log messages."""

import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """
    Obfuscates specified fields in the log message.

    Args:
        fields: List of strings representing fields to obfuscate.
        redaction: String to replace sensitive information with.
        message: String representing the log line.
        separator: String representing the character separating fields
        in the log line.

    Returns:
        Obfuscated log message.
    """
    pattern = f'({"|".join(map(re.escape, fields))})[^{separator}]*'
    return re.sub(pattern, f'\\1={redaction}', message)

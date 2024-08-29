#!/usr/bin/env python3
"""Module for obfuscating sensitive information in log messages."""

import re
from typing import List
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
                self.fields,
                self.REDACTION,
                record.getMessage(),
                self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

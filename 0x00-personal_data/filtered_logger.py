#!/usr/bin/env python3
"""
Module for obfuscating sensitive information in log messages.
"""

import re
import logging
from typing import List


def filter_datum(fields, redaction, message, separator):
    return re.sub(
        '|'.join([f'{field}=[^;]+' for field in fields]),
        lambda match: match.group().split('=')[0] + f'={redaction}',
        message
    )


class RedactingFormatter(logging.Formatter):
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )

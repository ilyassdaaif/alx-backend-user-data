#!/usr/bin/env python3
"""
Module for obfuscating sensitive information in log messages.
"""

import logging
import re
from typing import List

# Define PII_FIELDS as a tiple of PII field names
PII_FIELDS = ("name", "email", "ssn", "phone", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """Returns the log message obfuscated."""
    return re.sub(
        '|'.join([f'{field}=[^;]+' for field in fields]),
        lambda match: match.group().split('=')[0] + f'={redaction}',
        message
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

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

    def get_logger():
        """Creates and returns a logger."""
        logger = logging.getLogger("user_data")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        # Create a StreamHandler
        stream_handler = logging.StreamHandler()

        # Create a RedactingFormatter with PII_FIELDS
        formatter = RedactingFormatter(PII_FIELDS)

        # Set the formatter for the handler
        stream_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(stream_handler)

        return logger

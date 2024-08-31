#!/usr/bin/env python3
"""
Module for handling personal data
"""

from typing import List
import re
import logging
import mysql.connector
import os

# PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """
    Obfuscates specified fields in the log message.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database
    """
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError(
                "PERSONAL_DATA_DB_NAME environment variable is not set"
        )

    try:
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            raise Exception(
                    "Error: Access denied. Check your username and password."
            )
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            raise Exception(f"Error: Database '{db_name}' does not exist.")
        else:
            raise Exception(f"Error: {err}")


if __name__ == "__main__":
    logger = get_logger()
    logger.info("Sample log with PII data:name=John;email=john@example.com;"
                "ssn=123-45-6789;password=secret;")

#!/usr/bin/env python3
"""
Regex-ing
"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns a log message obfuscated with the string redaction"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message

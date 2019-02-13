# -*- coding: utf-8 -*-
import string


class CustomFormatter(string.Formatter):

    def __init__(self):
        super(CustomFormatter, self).__init__()

    def convert_field(self, value, conversion):
        # do any conversion on the resulting object
        if conversion is None:
            return value
        elif conversion == 's':
            return str(value)
        elif conversion == 'r':
            return repr(value)
        elif conversion == 'u':
            return value.upper()
        elif conversion == 'l':
            return value.lower()
        raise ValueError(
            "Unknown conversion specifier {0!s}".format(conversion))

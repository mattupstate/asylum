# -*- coding: utf-8 -*-
"""
    asylum._compat
    ~~~~~~~~~~~~~~

    Python compatability module
"""
import sys

PY2 = sys.version_info[0] == 2

if not PY2:
    text_type = str
    string_types = (str,)
else:
    text_type = unicode
    string_types = (str, unicode)

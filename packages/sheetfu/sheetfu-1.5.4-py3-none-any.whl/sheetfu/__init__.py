# -*- coding: utf-8 -*-

"""
    sheetfu
    ~~~~~~~

    A python library to interact with Google Sheets.
    :copyright: © 2018 by Social Point Labs.
    :license: MIT, see LICENSE for more details.
"""

# Important! Never update this version manually. The automatic semantic-releases library takes care of updating it #
# Manually changing this number could result in unexpected behaviour #
__version__ = "1.5.4"


from sheetfu.client import SpreadsheetApp
from sheetfu.modules.table import Table
from sheetfu.modules.table_selector import TableSelector



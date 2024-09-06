# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

from datetime import datetime

from django.test import TestCase

from .DateParser import get_date_help_text_from_dates, parse_date

help_text_default = "Dates are interpreted by defined rules. If this fails, an iso-date can be explicitly set with '&lt;YYYY-MM-DD&gt;'."


# helper function so we don't have to write as much
def fi(datestring):
    return datetime.fromisoformat(datestring)


# a dict of dates with the written date as key
# followed by a tuple of (single, start, end, help_text)
dates = {
    "vor dem 23.10.1449 <1449-10-23>": (
        fi("1449-10-23"),
        None,
        None,
        "Date interpreted as 1449-10-23",
    ),
    "1459-12": (
        fi("1459-12-16"),
        fi("1459-12-01"),
        fi("1459-12-31"),
        "Date interpreted as 1459-12-1 until 1459-12-31",
    ),
    "1460-03-30": (fi("1460-03-30"), None, None, "Date interpreted as 1460-3-30"),
    "": (
        None,
        None,
        None,
        "<b>Date could not be interpreted</b><br>" + help_text_default,
    ),
}


class DateParserTest(TestCase):
    def test_dates(self):
        for datestring, (expsingle, expstart, expend, help_text) in dates.items():
            single, start, end = parse_date(datestring)
            self.assertEqual(expsingle, single)
            self.assertEqual(expstart, start)
            self.assertEqual(expend, end)

    def test_help_text(self):
        for datestring, (single, start, end, exp_help_text) in dates.items():
            help_text = get_date_help_text_from_dates(single, start, end, datestring)
            self.assertEqual(exp_help_text, help_text)

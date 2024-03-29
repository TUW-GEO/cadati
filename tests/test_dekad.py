# Copyright (c) 2023, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module testing the dekad module.
"""

import unittest
import cadati.dekad as dk
from datetime import datetime


class Test(unittest.TestCase):

    def setUp(self):
        self.begin = datetime(2000, 1, 5)
        self.end = datetime(2000, 3, 15)

        self.date1 = datetime(2000, 2, 1)
        self.date2 = datetime(2000, 2, 13)
        self.date3 = datetime(2000, 2, 28)

    def tearDown(self):
        pass

    def test_dekad_index(self):
        firstdate = datetime(2000, 1, 10)
        lastdate = datetime(2000, 3, 20)
        items = 8

        dkindex = dk.dekad_index(self.begin, self.end)
        assert dkindex[0] == firstdate
        assert dkindex[-1] == lastdate
        assert dkindex.size == items

        dkindex = dk.dekad_index(self.begin)
        assert dkindex[0] == firstdate
        assert (dkindex[-1] - dk.check_dekad(datetime.now())).days == 0

        dkindex = dk.dekad_index(datetime(2014, 1, 3), datetime(2014, 1, 5))
        assert dkindex[0] == datetime(2014, 1, 10)
        assert dkindex.size == 1

        dkindex = dk.dekad_index(datetime(2014, 1, 3), datetime(2014, 1, 15))
        assert dkindex[0] == datetime(2014, 1, 10)
        assert dkindex[1] == datetime(2014, 1, 20)

        dkindex = dk.dekad_index(datetime(2014, 1, 3), datetime(2014, 1, 25))
        assert dkindex[0] == datetime(2014, 1, 10)
        assert dkindex[2] == datetime(2014, 1, 31)

        dkindex = dk.dekad_index(datetime(2014, 1, 13), datetime(2014, 1, 15))
        assert dkindex[0] == datetime(2014, 1, 20)
        assert dkindex.size == 1

        dkindex = dk.dekad_index(datetime(2014, 1, 13), datetime(2014, 1, 25))
        assert dkindex[0] == datetime(2014, 1, 20)
        assert dkindex[1] == datetime(2014, 1, 31)

        dkindex = dk.dekad_index(datetime(2014, 1, 23), datetime(2014, 1, 25))
        assert dkindex[0] == datetime(2014, 1, 31)
        assert dkindex.size == 1

        dkindex = dk.dekad_index(datetime(2014, 1, 3), datetime(2014, 3, 5))
        assert dkindex[0] == datetime(2014, 1, 10)
        assert dkindex[-1] == datetime(2014, 3, 10)

        dkindex = dk.dekad_index(datetime(2014, 1, 13), datetime(2014, 3, 25))
        assert dkindex[0] == datetime(2014, 1, 20)
        assert dkindex[-1] == datetime(2014, 3, 31)

    def test_check_dekad(self):

        dekad1 = dk.check_dekad(self.date1)
        dekad2 = dk.check_dekad(self.date2)
        dekad3 = dk.check_dekad(self.date3)

        assert dekad1 == datetime(2000, 2, 10)
        assert dekad2 == datetime(2000, 2, 20)
        assert dekad3 == datetime(2000, 2, 29)

    def test_dekad2day(self):

        assert dk.dekad2day(2000, 2, 1) == 10
        assert dk.dekad2day(2000, 2, 2) == 20
        assert dk.dekad2day(2000, 2, 3) == 29

    def test_day2dekad(self):

        dekad = dk.day2dekad(29)

        assert dekad == 3

    def test_get_dekad_period(self):

        dates = [self.date1, self.date2, self.date3]

        periods = dk.get_dekad_period(dates)

        assert periods == [4, 5, 6]

    def test_runningdekad2date(self):
        assert dk.runningdekad2date(2014, 35) == datetime(2014, 12, 20)


def test_check_dekad_startdate():
    assert dk.check_dekad_startdate(datetime(2000, 1, 1))
    assert dk.check_dekad_startdate(datetime(2000, 1, 11))
    assert dk.check_dekad_startdate(datetime(2000, 1, 21))
    assert not dk.check_dekad_startdate(datetime(2000, 1, 22))


def test_check_dekad_enddate():
    assert dk.check_dekad_enddate(datetime(2000, 1, 10))
    assert dk.check_dekad_enddate(datetime(2000, 1, 20))
    assert dk.check_dekad_enddate(datetime(2000, 1, 31))
    assert dk.check_dekad_enddate(datetime(2000, 2, 29))
    assert not dk.check_dekad_enddate(datetime(2000, 2, 28))


def test_dekad_startdate_from_date():
    assert datetime(2000, 1, 1) == dk.dekad_startdate_from_date(
        datetime(2000, 1, 10))
    assert datetime(2000, 2, 21) == dk.dekad_startdate_from_date(
        datetime(2000, 2, 29))
    assert datetime(2000, 2, 11) == dk.dekad_startdate_from_date(
        datetime(2000, 2, 17))


def test_group_into_dekads():
    dtimes = [datetime(2000, 1, 10),
              datetime(2000, 1, 11),
              datetime(2000, 1, 12),
              datetime(2000, 1, 23)]
    groups = dk.group_into_dekads(dtimes)
    assert groups == {datetime(2000, 1, 10): [datetime(2000, 1, 10)],
                      datetime(2000, 1, 20): [datetime(2000, 1, 11),
                                              datetime(2000, 1, 12)],
                      datetime(2000, 1, 31): [datetime(2000, 1, 23)]}
    groups = dk.group_into_dekads(dtimes,
                                  use_dekad_startdate=True)
    assert groups == {datetime(2000, 1, 1): [datetime(2000, 1, 10)],
                      datetime(2000, 1, 11): [datetime(2000, 1, 11),
                                              datetime(2000, 1, 12)],
                      datetime(2000, 1, 21): [datetime(2000, 1, 23)]}

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

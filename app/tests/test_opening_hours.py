import unittest
from datetime import datetime

from campusroute.opening_hours import is_open


class OpeningHoursTest(unittest.TestCase):
    def test_open_standard(self):
        # 1 March 2027 is a Monday
        mon_morning = datetime(2027, 3, 1, 9, 30)
        self.assertTrue(is_open("Mon-Fri 08:00-17:00", mon_morning))

    def test_closed_weekend(self):
        sat_morning = datetime(2027, 3, 6, 9, 30)
        self.assertFalse(is_open("Mon-Fri 08:00-17:00", sat_morning))

    def test_midnight_24_00(self):
        mon_night = datetime(2027, 3, 1, 23, 30)
        self.assertTrue(is_open("Mon 08:00-24:00", mon_night))

    def test_overnight_span(self):
        fri_night = datetime(2027, 3, 5, 23, 30)
        sat_early = datetime(2027, 3, 6, 1, 30)
        sat_late = datetime(2027, 3, 6, 3, 30)
        hours = "Fri 20:00-02:00"
        self.assertTrue(is_open(hours, fri_night))
        self.assertTrue(is_open(hours, sat_early))
        self.assertFalse(is_open(hours, sat_late))


if __name__ == "__main__":
    unittest.main()

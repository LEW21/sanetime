import unittest2 as unittest
from datetime import datetime
import pytz
from .. import time
from ..error import TimeConstructionError

# IMPORTANT -- note to self -- you CANNOT use tzinfo on datetime-- ever! -- just pytz.timezone.localize everything to be safe

JAN_MICROS = 1325376000*1000**2
JAN_MILLIS = JAN_MICROS//1000
JAN_SECS = JAN_MILLIS//1000
JAN_MINS = JAN_SECS//60
JUL_MICROS = 1338508800*1000**2
HOUR_MICROS = 60**2*1000**2

NY_JAN_MICROS = JAN_MICROS + HOUR_MICROS * 5
NY_JUL_MICROS = JUL_MICROS + HOUR_MICROS * 4

LA_JAN_MICROS = JAN_MICROS + HOUR_MICROS * 8
LA_JUL_MICROS = JUL_MICROS + HOUR_MICROS * 7

TZ_UTC = pytz.utc
TZ_NY = pytz.timezone('America/New_York')
TZ_LA = pytz.timezone('America/Los_Angeles')
TZ_AC = pytz.timezone('Africa/Cairo')

class SaneTimeTest(unittest.TestCase):

    def assertSaneTimeEquals(self, st1, st2):
        self.assertInnards(st1.us, st1.tz, st2)

    def setUp(self):
        pass


    def test_microsecond_construction(self):
        self.assertEqual((JAN_MICROS,TZ_UTC), time(JAN_MICROS)._tuple)
        for kwarg in ('us','micros','microseconds','epoch_micros','epoch_microseconds'):
            self.assertEqual((JAN_MICROS,TZ_UTC), time(**{kwarg:JAN_MICROS})._tuple)
            self.assertEqual(JAN_MICROS, getattr(time(**{kwarg:JAN_MICROS}),kwarg))
        for kwarg in ('ms','millis','milliseconds','epoch_millis','epoch_milliseconds'):
            self.assertEqual((JAN_MICROS,TZ_UTC), time(**{kwarg:JAN_MILLIS})._tuple)
            self.assertEqual(JAN_MILLIS, getattr(time(**{kwarg:JAN_MILLIS}),kwarg))
        for kwarg in ('s','secs','seconds','epoch_secs','epoch_seconds'):
            self.assertEqual((JAN_MICROS,TZ_UTC), time(**{kwarg:JAN_SECS})._tuple)
            self.assertEqual(JAN_SECS, getattr(time(**{kwarg:JAN_SECS}),kwarg))
        for kwarg in ('m','mins','minutes','epoch_mins','epoch_minutes'):
            self.assertEqual((JAN_MICROS,TZ_UTC), time(**{kwarg:JAN_MINS})._tuple)
            self.assertEqual(JAN_MINS, getattr(time(**{kwarg:JAN_MINS}),kwarg))

    def test_timezone_construction(self):
        self.assertEqual((JAN_MICROS,TZ_NY), time(JAN_MICROS,'America/New_York')._tuple)
        self.assertEqual((JAN_MICROS,TZ_NY), time(JAN_MICROS,TZ_NY)._tuple)
        self.assertEqual((JAN_MICROS,TZ_NY), time(JAN_MICROS,tz=TZ_NY)._tuple)
        self.assertEqual((JAN_MICROS,TZ_NY), time(s=JAN_SECS,timezone='America/New_York')._tuple)
        self.assertEqual(TZ_UTC, time(tz=TZ_UTC).tz)
        self.assertEqual(TZ_NY, time(tz='America/New_York').tz)

        # nomal string
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00')._tuple)
        self.assertEqual((JUL_MICROS,TZ_UTC), time('2012-06-01 00:00:00')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00','UTC')._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time('2012-01-01 00:00:00','America/New_York')._tuple)

        # Z terminus
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01T00:00:00Z')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01T00:00:00Z','UTC')._tuple)
        with self.assertRaises(TimeConstructionError): time('2012-01-01T00:00:00Z','America/New_York') # conflicting timezones

        # offset terminus
        self.assertEqual((NY_JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00-05:00')._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00-05:00','UTC')._tuple) # conflicting timezones
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time('2012-01-01 00:00:00-05:00','America/New_York')._tuple)

        # tz abbr -- parse can't handle these, so we have to rely on timezones entirely
        self.assertEqual((JUL_MICROS,TZ_UTC), time('2012-06-01 00:00:00 EDT')._tuple)
        self.assertEqual((NY_JUL_MICROS,TZ_NY), time('2012-06-01 00:00:00 EDT','America/New_York')._tuple)
        self.assertEqual((JUL_MICROS,TZ_UTC), time('2012-06-01 00:00:00 PDT')._tuple)
        self.assertEqual((LA_JUL_MICROS,TZ_LA), time('2012-06-01 00:00:00 PDT','America/Los_Angeles')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00 EST','UTC')._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time('2012-01-01 00:00:00 EST','America/New_York')._tuple)

    def test_now_construction(self):
        self.assertTrue(time('2012-04-28') < time() < time('2038-01-01'))  # i'm assuming this library will no longer be needed after 2038 cuz we'll have flying cars by then, finally!
        self.assertTrue(time() < time(tz=TZ_UTC) < time(tz=TZ_NY) < time(tz=TZ_UTC) < time())

    def test_string_parsing(self):
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01T00:00Z')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00+00:00')._tuple)
        self.assertEqual((JAN_MICROS-HOUR_MICROS,TZ_UTC), time('2012-01-01 00:00:00+01:00')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('Sunday, January 1st 2012, at 12:00am')._tuple)

        # tz included
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 +UTC')._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time('2012-01-01 +America/New_York')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00 +UTC')._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time('2012-01-01 00:00:00 +America/New_York')._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time('2012-01-01 00:00:00.000000 +UTC')._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time('2012-01-01 00:00:00.000000 +America/New_York')._tuple)

    def test_bad_construction(self):
        with self.assertRaises(TimeConstructionError): self.assertTrue(JAN_MICROS, time(unknown=None))

    def test_datetime_construction(self):
        self.assertEqual((JAN_MICROS,TZ_UTC), time(datetime(2012,1,1))._tuple)
        self.assertEqual((JAN_MICROS+10**6*60**2,TZ_UTC), time(datetime(2012,1,1,1))._tuple)
        self.assertEqual((JAN_MICROS+10**6*60,TZ_UTC), time(datetime(2012,1,1,0,1))._tuple)
        self.assertEqual((JAN_MICROS+10**6,TZ_UTC), time(datetime(2012,1,1,0,0,1))._tuple)
        self.assertEqual((JAN_MICROS+1,TZ_UTC), time(datetime(2012,1,1,0,0,0,1))._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time(datetime(2012,1,1,0,0,0,0,None))._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time(datetime(2012,1,1,0,0,0,0,TZ_NY))._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time(datetime(2012,1,1,0,0,0,0,TZ_UTC))._tuple)

        # mimic datetime constructor as well
        self.assertEqual((JAN_MICROS,TZ_UTC), time(2012,1,1)._tuple)
        self.assertEqual((JAN_MICROS+10**6*60**2,TZ_UTC), time(2012,1,1,1)._tuple)
        self.assertEqual((JAN_MICROS+10**6*60,TZ_UTC), time(2012,1,1,0,1)._tuple)
        self.assertEqual((JAN_MICROS+10**6,TZ_UTC), time(2012,1,1,0,0,1)._tuple)
        self.assertEqual((JAN_MICROS+1,TZ_UTC), time(2012,1,1,0,0,0,1)._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time(2012,1,1,0,0,0,0,None)._tuple)
        self.assertEqual((NY_JAN_MICROS,TZ_NY), time(2012,1,1,0,0,0,0,TZ_NY)._tuple)
        self.assertEqual((JAN_MICROS,TZ_UTC), time(2012,1,1,0,0,0,0,TZ_UTC)._tuple)

    def test_copy_construction(self):
        self.assertEqual((JAN_MICROS,TZ_UTC), time(time(JAN_MICROS,TZ_UTC))._tuple)
        self.assertEqual((JAN_MICROS,TZ_NY), time(time(JAN_MICROS,TZ_NY))._tuple)

    def test_clone(self):
        self.assertEqual((JAN_MICROS,TZ_UTC), time(JAN_MICROS,TZ_UTC).clone()._tuple)
        self.assertEqual((JAN_MICROS,TZ_NY), time(JAN_MICROS,TZ_NY).clone()._tuple)

    def test_casting(self):
        self.assertEqual(JAN_MICROS, int(time(JAN_MICROS)))
        self.assertEqual(JAN_MICROS, int(time(JAN_MICROS)))
        self.assertEqual('2012-01-01 +UTC', str(time(JAN_MICROS)))
        self.assertEqual('2012-01-01 +UTC', str(time(JAN_MICROS)))
        self.assertEqual('2012-01-01 00:00:01 +UTC', str(time(JAN_MICROS+10**6)))
        self.assertEqual('2012-01-01 00:00:00.000001 +UTC', str(time(JAN_MICROS+1)))
        self.assertEqual(hash(JAN_MICROS), hash(time(JAN_MICROS)))

    def test_equality(self):
        t1 = time(JAN_MICROS, tz='UTC')
        t2 = time(JAN_MICROS, tz='America/New_York')
        t3 = time(JAN_MICROS+1)
        self.assertTrue(t1==t2)
        self.assertTrue(t2==t1)
        self.assertTrue(t1!=t3)
        self.assertTrue(t3!=t1)

        self.assertFalse(t1!=t2)
        self.assertFalse(t2!=t1)
        self.assertFalse(t1==t3)
        self.assertFalse(t3==t1)

        self.assertTrue(t1!=None)
        self.assertFalse(t1==None)
        self.assertTrue(None!=t1)
        self.assertFalse(None==t1)

        self.assertTrue(t1==t1.us)

    def test_comparisons(self):
        t1 = time(JAN_MICROS)
        t2 = time(JAN_MICROS+1)

        self.assertFalse(t1 > t1)
        self.assertTrue(t2 > t1)
        self.assertFalse(t1 > t2)

        self.assertTrue(t1 >= t1)
        self.assertTrue(t2 >= t1)
        self.assertFalse(t1 >= t2)

        self.assertFalse(t1 < t1)
        self.assertFalse(t2 < t1)
        self.assertTrue(t1 < t2)

        self.assertTrue(t1 <= t1)
        self.assertFalse(t2 <= t1)
        self.assertTrue(t1 <= t2)

    def test_transitives(self):
        st = time(tz='America/New_York')
        self.assertEqual(st._tuple, time(st.datetime)._tuple)
        self.assertEqual(st.us, time(int(st)).us)
        self.assertEqual(st._tuple, time(str(st))._tuple)
        self.assertEqual(st._tuple, time(st)._tuple)

    def test_hashability(self):
        t1 = time(JAN_MICROS, tz='UTC')
        t2 = time(JAN_MICROS, tz='America/New_York')
        t3 = time(JAN_MICROS+1)
        s = set([t1,t2,t3])
        self.assertEqual(2, len(s))
        self.assertIn(t1, s)
        self.assertIn(t2, s)
        self.assertIn(t3, s)

    def test_arithmetic(self):
        t1 = time(JAN_MICROS)
        t2 = time(JAN_MICROS+1)

        self.assertEqual(t2.us, (t1+1).us)
        self.assertEqual(t1.us,(t2-1).us)

        self.assertEqual(1, t2 - t1)
        self.assertEqual(-1, t1 - t2)

        self.assertEqual(t1.us,t1*1)
        self.assertEqual(t1.us,t1/1)

    def test_datetime_properties(self):
        self.assertEqual(datetime(2012,1,1,tzinfo=TZ_UTC),time(JAN_MICROS,TZ_UTC).datetime)
        self.assertEqual(datetime(2012,1,1,tzinfo=TZ_NY),time(NY_JAN_MICROS,TZ_NY).datetime)

        self.assertEqual(datetime(2012,1,1),time(JAN_MICROS,TZ_UTC).naive_datetime)
        self.assertEqual(datetime(2012,1,1),time(NY_JAN_MICROS,TZ_NY).naive_datetime)

        self.assertEqual(datetime(2012,1,1,tzinfo=TZ_UTC),time(JAN_MICROS,TZ_UTC).utc_datetime)
        self.assertEqual(datetime(2012,1,1,tzinfo=TZ_UTC),time(JAN_MICROS,TZ_NY).utc_datetime)

        self.assertEqual(datetime(2012,1,1),time(JAN_MICROS,TZ_UTC).utc_naive_datetime)
        self.assertEqual(datetime(2012,1,1),time(JAN_MICROS,TZ_NY).utc_naive_datetime)

        self.assertEqual(datetime(2012,1,1,tzinfo=TZ_NY),time(NY_JAN_MICROS,TZ_UTC).ny_datetime)
        self.assertEqual(datetime(2012,1,1,tzinfo=TZ_NY),time(NY_JAN_MICROS,TZ_NY).ny_datetime)

        self.assertEqual(datetime(2012,1,1),time(NY_JAN_MICROS,TZ_UTC).ny_naive_datetime)
        self.assertEqual(datetime(2012,1,1),time(NY_JAN_MICROS,TZ_NY).ny_naive_datetime)

    def test_switching_timezones(self):
        t1 = time(JAN_MICROS)
        self.assertEqual(pytz.timezone('America/New_York'), t1.with_tz('America/New_York').tz)
        self.assertEqual(t1, time(t1).set_tz('America/New_York'))
        self.assertEqual(t1, t1.with_tz('America/New_York'))
        self.assertNotEqual(t1.tz, time(t1).set_tz('America/New_York').tz)
        self.assertNotEqual(t1.tz, t1.with_tz('America/New_York').tz)
        self.assertEqual(pytz.timezone('America/New_York'), time(t1).set_tz('America/New_York').tz)
        self.assertEqual(pytz.timezone('America/New_York'), t1.with_tz('America/New_York').tz)
        t1_id = id(t1)
        self.assertEqual(t1_id, id(t1.set_tz('America/New_York')))
        self.assertNotEqual(t1_id, id(t1.with_tz('America/New_York')))



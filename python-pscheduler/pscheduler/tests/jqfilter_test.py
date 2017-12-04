"""
test for the JQFilter module.
"""

import unittest

from base_test import PschedTestBase

from pscheduler.jqfilter import JQFilter


class TestJQFilter(PschedTestBase):
    """
    JQFilter tests.
    """

    def test_string(self):
        """Test a string filter"""

        f = JQFilter(".")
        self.assertEqual(f({"abc": 123})[0], {"abc": 123 })


    def test_array(self):
        """Test an array filter"""

        f = JQFilter([ "", ".", "", ""])
        self.assertEqual(f({"abc": 123})[0], {"abc": 123 })


    def test_array_empty(self):
        """Test an empty array filter"""

        f = JQFilter([])
        self.assertEqual(f({"abc": 123})[0], {"abc": 123 })


    def test_hash(self):
        """Test a hash filter"""

        f = JQFilter({"script": "."})
        self.assertEqual(f({"abc": 123})[0], {"abc": 123 })


    def test_hash_array(self):
        """Test a hash filter with an array script"""

        f = JQFilter({"script": [ "", ".", "", ""]})
        self.assertEqual(f({"abc": 123})[0], {"abc": 123 })


    def test_wrong_type(self):
        """Test a wrongly-typed filter"""

        with self.assertRaises(ValueError):
            f = JQFilter(1234)


    def test_bad_syntax(self):
        """Text a filter with the wrong syntax"""

        with self.assertRaises(ValueError):
            f = JQFilter("this is bad")



if __name__ == '__main__':
    unittest.main()

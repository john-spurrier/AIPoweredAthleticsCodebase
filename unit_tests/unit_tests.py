import unittest
"""
Unit testing file
"""

class UnitTests(unittest.TestCase):
    """
    Class containing unit tests.

    Unit tests can be added here by creating a new function and adding your specific test.
    """

    def test_sample(self):
        """
        Sample unit testing function, tests 1=1
        """

        self.assertEqual(1, 1, 'Nums are not equal')

if __name__ == '__main__':
    unittest.main()
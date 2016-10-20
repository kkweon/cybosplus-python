import unittest

from API.main import CybosPlus


class TestCase(unittest.TestCase):
    CybosPlus.initialize("0302", 0)

    def test_connection(self):
        self.assertEqual(CybosPlus.is_connected(), 1, "Connection Test")

    def test_get_account_number(self):
        account_number = CybosPlus.get_account_number()
        self.assertTrue(len(account_number) > 0, "Returned Account Number: {}".format(account_number))


if __name__ == "__main__":
    unittest.main()

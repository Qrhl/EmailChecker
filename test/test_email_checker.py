import unittest
from EmailChecker import *

class TestEmailChecker(unittest.TestCase):

    def setUp(self):
        self.email = EmailChecker("contact@smartbuild.asia")
        self.email_wrg_format = EmailChecker("test@test")
        self.email_wrg_domain = EmailChecker("contact@smartbuild.asi")
        self.email_wrg_user = EmailChecker("co@smartbuild.asia")

    def test_valid_format(self):
        self.assertTrue(self.email.valid_format())
        with self.assertRaises(WrongFormatException):
            self.email_wrg_format.valid_format()

    def test_valid_email(self):
        self.assertTrue(self.email.valid_email())

        with self.assertRaises(NoSuchDomainException):
            self.email_wrg_domain.valid_email()

        with self.assertRaises(NoSuchUserException):
            self.email_wrg_user.valid_email()

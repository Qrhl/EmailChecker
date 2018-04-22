import re
import dns.resolver
import telnetlib


class WrongFormatException(Exception):
    """
    Exception raised if the email address does not match the regex in the class EmailChecker
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "The email address does not have the good format"


class NoSuchDomainException(Exception):
    """
    Exception raised if the domain of the email address does not exist
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "The domain of the email does not exist or does not respond"


class NoSuchUserException(Exception):
    """
    Exception raised if the user in the email address does not exist
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "The user of this email does not exist"


class EmailChecker:
    """
    Usage in a script:
        checker = EmailChecker("@emailtotest")
        try:
            if checker.valid_email():
                ...
        except WrongFormatException:
            ...
        except NoSuchDomainException:
            ...
        except NoSuchUserException:
            ...
        
    It return true if valid, raise an exception otherwise. The exception raised allows to identify the issue
    """

    email_regex = re.compile(r"^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+\.?[a-zA-Z]{2,3}$")

    def __init__(self, address=""):
        """
        Simple constructor for the object
        :param address: Address to verify
        """
        self.address = address
        self.domain = ""

    def valid_format(self):
        """
        This function checks whether the email address is valid or not (matches the regex)
        :return: True or raise an exception
        """
        if EmailChecker.email_regex.match(self.address):
            self.domain = self.address.split('@')[1]
            return True
        raise WrongFormatException

    def valid_domain(self,domain_arg=''):
        """
        Check if the domain associated to the email address exists
        :return: The address of the MX registration (SMTP server) or raise an exception
        """
        list_mx = []
        domain_mx = ''

        if domain_arg != '':
            domain_mx = domain_arg
        else:
            domain_mx = self.domain

        try:
            for mx in dns.resolver.query(domain_mx, 'MX'):
                list_mx.append(str(mx).split(' '))
        except dns.resolver.NXDOMAIN:
            raise NoSuchDomainException
        except dns.resolver.NoAnswer:
            raise NoSuchDomainException
        return list_mx[0][1]

    def valid_user(self, mx_address):
        """
        Checks if the user of the email address exists
        :param mx_address: Address of the SMTP server
        :return: True or raise an exception
        """
        try:
            conn_tel = telnetlib.Telnet(mx_address, 25)
            conn_tel.read_until(b"\r").decode()
            conn_tel.write("helo qrhl\r\n".encode("utf-8"))
            conn_tel.read_until(b"\r").decode()
            conn_tel.write("mail from:<test@rate.pi>\r\n".encode("utf-8"))
            conn_tel.read_until(b"\r").decode()
            rcpt_to = "rcpt to:<{0}>\r\n)".format(self.address)
            conn_tel.write(rcpt_to.encode("utf-8"))
            response = conn_tel.read_until(b"\r").decode()
        except Exception as e:
            print(e)
        if response.find("250") != -1:
            return True
        else:
            raise NoSuchUserException

    def valid_email(self):
        """
        Uses the methods above to do a complete check of the email address
        :return: True or raise an exception
        """
        try:
            self.valid_format()
            domain = self.valid_domain()
            self.valid_user(domain)
        except Exception as e:
            raise e
        return True


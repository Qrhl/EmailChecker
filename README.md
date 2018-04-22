# EmailChecker

Usage:

```python
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
```
It returns true if valid, raise an exception otherwise. The exception raised allows to identify the issue

It is also possible to use the different methods of the class in order to check only one step.

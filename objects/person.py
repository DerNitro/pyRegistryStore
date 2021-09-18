"""
    Example plugin Person
"""
from datetime import datetime
from objects import RegistryStore, now

class Person(RegistryStore):
    """
    Person Object

    Parameters
    ----------
    first_name: str
        First Name
    last_name: str
        Last Name
    """
    _uniq_key = ['first_name', 'last_name']
    _desc = 'Module Person'

    first_name:     str = 'Foo'
    last_name:      str = 'Bar'
    sex:            str = ''
    create_date:    datetime = now()

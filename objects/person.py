"""
    Example plugin Person
"""
import objects


class Person(objects.RegistryStore):
    """
    Person Object

    Parameters
    ----------
    first_name: str
        First Name
    last_name: str
        Last Name
    """
    uniq_key = ['first_name', 'last_name']
    desc = 'Module Person'

    first_name: str = 'Foo'
    last_name:  str = 'Bar'
    sex:        str = ''

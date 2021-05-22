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

    first_name = None
    last_name = None

    def __init__(self) -> None:
        super().__init__()
        self.first_name = 'Foo'
        self.last_name = 'Bar'

    def describe(self):
        return str('Module Person')

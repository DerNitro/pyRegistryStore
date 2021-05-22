import yaml
import os
from datetime import datetime
import uuid
import json


class Meta(yaml.YAMLObject):
    def __init__(self):
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.version = 1
        self.uuid = uuid.uuid4()

    def __repr__(self):
        return str(
            {
                "create_time": str(self.create_time),
                "update_time": str(self.update_time),
                "version": self.version,
                "uuid": str(self.uuid)
            }
        )

    def __str__(self) -> str:
        return str(self.__dict__)

    def increment(self):
        self.version += 1
        self.update_time = datetime.now()

    def to_dict(self):
        return dict(
            {
                "create_time": str(self.create_time),
                "update_time": str(self.update_time),
                "version": self.version,
                "uuid": str(self.uuid)
            }
        )


class RegistryStore(yaml.YAMLObject):
    _meta = None
    file_name = None
    uniq_key = None

    def __init__(self) -> None:
        self._meta = Meta()

    def describe(self) -> str:
        """
        Brief description of the module, used in LS
        """
        pass

    def help(self) -> str:
        return str(self.__class__.__doc__)

    def add_attr(self, key, value):
        setattr(self, key, value)

    def get_filename(self):
        if self.file_name:
            return self.file_name
        else:
            return str(self.__class__.__name__).lower() + '.yml'

    def to_dict(self):
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, Meta):
                result[k] = v.to_dict()
                pass
            else:
                result[k] = v
        return result

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for uniq_key in self.uniq_key:
                if getattr(self, uniq_key) != getattr(other, uniq_key):
                    return False
            return True

        return False

    def __lt__(self, other):
        return self._meta.update_time < other._meta.update_time


def auto_type(value):
    try:
        return(int(value))
    except ValueError:
        pass

    if str(value).lower() in ['true', 'y', 'yes']:
        return True

    if str(value).lower() in ['false', 'f', 'no']:
        return False

    return value


def equal_object(obj: RegistryStore, args: list):
    for arg in args:
        key, value = str(arg).split('=')
        if getattr(obj, key, None) != value:
            return False
    return True


def print_json(data):
    if isinstance(data, list):
        results = []
        for obj in data:
            results.append(obj.to_dict())
        print(json.dumps(results))
    if isinstance(data, RegistryStore):
        print(json.dumps(data.to_dict()))


def set(object: RegistryStore, folder, args):
    obj_list = []
    o = object()
    for arg in args:
        key, value = str(arg).split('=')
        o.add_attr(key, auto_type(value))

    file_name = os.path.join(folder, o.get_filename())
    if os.path.isfile(file_name):
        with open(file_name, 'r') as stream:
            obj_list = yaml.load(stream, Loader=yaml.CLoader)
        if o in obj_list:
            indx = obj_list.index(o)
            o = obj_list.pop(indx)
            o._meta.increment()
            for arg in args:
                key, value = str(arg).split('=')
                o.add_attr(key, auto_type(value))
            obj_list.append(o)
        else:
            obj_list.append(o)
    else:
        obj_list.append(o)

    with open(file_name, 'w') as stream:
        stream.write(yaml.dump(obj_list, Dumper=yaml.CDumper))


def get(object, folder, args):
    o = object()
    result = []
    file_name = os.path.join(folder, o.get_filename())
    if os.path.isfile(file_name):
        with open(file_name, 'r') as stream:
            obj_list = yaml.load(stream, Loader=yaml.CLoader)
        for obj in obj_list:
            if equal_object(obj, args):
                result.append(obj)
        print_json(result)
    else:
        pass


def last(object, folder, args):
    o = object()
    result = []
    file_name = os.path.join(folder, o.get_filename())
    if os.path.isfile(file_name):
        with open(file_name, 'r') as stream:
            obj_list = yaml.load(stream, Loader=yaml.CLoader)
        for obj in obj_list:
            if equal_object(obj, args):
                result.append(obj)
        print_json(sorted(result, reverse=True)[0])
    else:
        pass


def help(object):
    o = object()
    print(o.help())

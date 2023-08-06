from functools import wraps
from threading import RLock
from types import FunctionType, MethodType

from graphility.database import Database
from graphility.database_safe_shared import th_safe_gen
from graphility.env import cdb_environment

cdb_environment["mode"] = "threads"
cdb_environment["rlock_obj"] = RLock


class SuperLock(type):
    @staticmethod
    def wrapper(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            db = args[0]
            with db.super_lock:
                #                print '=>', f.__name__, repr(args[1:])
                res = f(*args, **kwargs)
                #                if db.opened:
                #                    db.flush()
                #                print '<=', f.__name__, repr(args[1:])
                return res

        return _inner

    def __new__(cls, classname, bases, attr):
        new_attr = {}
        for base in bases:
            for b_attr in dir(base):
                a = getattr(base, b_attr, None)
                if isinstance(a, MethodType) and not b_attr.startswith("_"):
                    if b_attr in ("flush", "flush_indexes"):
                        pass
                    else:
                        # setattr(base, b_attr, SuperLock.wrapper(a))
                        new_attr[b_attr] = SuperLock.wrapper(a)
        for attr_name, attr_value in attr.items():
            if isinstance(attr_value, FunctionType) and not attr_name.startswith("_"):
                attr_value = SuperLock.wrapper(attr_value)
            new_attr[attr_name] = attr_value
        new_attr["super_lock"] = RLock()
        return type.__new__(cls, classname, bases, new_attr)


class SuperThreadSafeDatabase(Database, metaclass=SuperLock):
    """
    Thread safe version that always allows single thread to use db.
    It adds the same lock for all methods, so only one operation can be
    performed in given time. Completely different implementation
    than ThreadSafe version (without super word)
    """

    __metaclass__ = SuperLock

    def __patch_index_gens(self, name):
        ind = self.indexes_names[name]
        for c in ("all", "get_many"):
            m = getattr(ind, c)
            if getattr(ind, c + "_orig", None):
                return
            m_fixed = th_safe_gen.wrapper(m, name, c, self.super_lock)
            setattr(ind, c, m_fixed)
            setattr(ind, c + "_orig", m)

    def open(self, *args, **kwargs):
        res = super(SuperThreadSafeDatabase, self).open(*args, **kwargs)
        for name, _ in self.indexes_names.items():
            self.__patch_index_gens(name)
        return res

    def create(self, *args, **kwargs):
        res = super(SuperThreadSafeDatabase, self).create(*args, **kwargs)
        for name, _ in self.indexes_names.items():
            self.__patch_index_gens(name)
            return res

    def add_index(self, *args, **kwargs):
        res = super(SuperThreadSafeDatabase, self).add_index(*args, **kwargs)
        self.__patch_index_gens(res)
        return res

    def edit_index(self, *args, **kwargs):
        res = super(SuperThreadSafeDatabase, self).edit_index(*args, **kwargs)
        self.__patch_index_gens(res)
        return res

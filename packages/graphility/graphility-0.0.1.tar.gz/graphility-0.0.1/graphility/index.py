import marshal
import os
import shutil
import struct

from graphility.storage import DummyStorage, IU_Storage

try:
    from graphility import __version__
except ImportError:
    from __init__ import __version__

import io


class IndexException(Exception):
    pass


class IndexNotFoundException(IndexException):
    pass


class ReindexException(IndexException):
    pass


class TryReindexException(ReindexException):
    pass


class ElemNotFound(IndexException):
    pass


class DocIdNotFound(ElemNotFound):
    pass


class IndexConflict(IndexException):
    pass


class IndexPreconditionsException(IndexException):
    pass


class Index:

    __version__ = __version__

    STATUS_O = b"o"
    STATUS_U = b"u"
    STATUS_D = b"d"

    custom_header = ""  # : use it for imports required by your index

    def __init__(self, db_path, name):
        self.name = name
        self._start_ind = 500
        self.db_path = db_path
        # self.storage = None

    def open_index(self):
        if not os.path.isfile(os.path.join(self.db_path, self.name + "_buck")):
            raise IndexException("Doesn't exists")
        self.buckets = io.open(
            os.path.join(self.db_path, self.name + "_buck"), "r+b", buffering=0
        )
        self._fix_params()
        self._open_storage()

    def _close(self):
        self.buckets.close()
        self.storage.close()

    def close_index(self):
        self.flush()
        self.fsync()
        self._close()

    def create_index(self):
        raise NotImplementedError()

    def _fix_params(self):
        self.buckets.seek(0)
        props = marshal.loads(self.buckets.read(self._start_ind))
        for k, v in props.items():
            self.__dict__[k] = v
        self.buckets.seek(0, 2)

    def _save_params(self, in_params={}):
        self.buckets.seek(0)
        props = marshal.loads(self.buckets.read(self._start_ind))
        props.update(in_params)
        self.buckets.seek(0)
        data = marshal.dumps(props)
        if len(data) > self._start_ind:
            raise IndexException("To big props")
        self.buckets.write(data)
        self.flush()
        self.buckets.seek(0, 2)
        self.__dict__.update(props)

    def _open_storage(self, *args, **kwargs):
        pass

    def _create_storage(self, *args, **kwargs):
        pass

    def _destroy_storage(self, *args, **kwargs):
        self.storage.destroy()

    def _find_key(self, key):
        raise NotImplementedError()

    def update(self, doc_id, key, start, size):
        raise NotImplementedError()

    def insert(self, doc_id, key, start, size):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def get_many(self, key, start_from=None, limit=0):
        raise NotImplementedError()

    def all(self, start_pos):
        raise NotImplementedError()

    def delete(self, key, start, size):
        raise NotImplementedError()

    def make_key_value(self, data):
        raise NotImplementedError()

    def make_key(self, data):
        raise NotImplementedError()

    def compact(self, *args, **kwargs):
        raise NotImplementedError()

    def destroy(self, *args, **kwargs):
        self._close()
        bucket_file = os.path.join(self.db_path, self.name + "_buck")
        os.unlink(bucket_file)
        self._destroy_storage()
        self._find_key.clear()

    def flush(self):
        try:
            self.buckets.flush()
            self.storage.flush()
        except:
            pass

    def fsync(self):
        try:
            os.fsync(self.buckets.fileno())
            self.storage.fsync()
        except:
            pass

    def update_with_storage(self, doc_id, key, value):
        if value:
            start, size = self.storage.insert(value)
        else:
            start = 1
            size = 0
        return self.update(doc_id, key, start, size)

    def insert_with_storage(self, doc_id, key, value):
        if value:
            start, size = self.storage.insert(value)
        else:
            start = 1
            size = 0
        return self.insert(doc_id, key, start, size)

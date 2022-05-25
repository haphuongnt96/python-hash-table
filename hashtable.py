import enum
from typing import AnyStr, NamedTuple, Any
from collections import deque

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:
    @classmethod
    def from_dict(cls, dictionary: dict, capacity: int = None):
        hash_table = cls(capacity or len(dictionary))
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table

    def __init__(self, capacity=8, load_factor_threshold=0.6):
        if capacity <= 0:
            raise ValueError('Capacity must be a positive number!')
        if not (0 < load_factor_threshold <= 1):
            raise ValueError('Load factor must be a number between (0, 1]')
        # self._slots = capacity * [None]
        self._keys = []
        self._buckets = [deque() for _ in range(capacity)]
        self._load_factor_threshold = load_factor_threshold

    def __len__(self):
        return len(self.pairs)

    def __setitem__(self, key, value):
        if self.load_factor >= self._load_factor_threshold:
            self._resize_and_rehash()

        bucket = self._buckets[self._index(key)]
        for index, pair in enumerate(bucket):
            if pair.key == key:
                bucket[index] = Pair(key, value)
                break
        else:
            bucket.append(Pair(key, value))
            self._keys.append(key)

    def __getitem__(self, key):
        bucket = self._buckets[self._index(key)]
        for pair in bucket:
            if pair.key == key:
                return pair.value
        raise KeyError(key)
    
    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key):
        bucket = self._buckets[self._index(key)]
        for index, pair in enumerate(bucket):
            if pair.key == key:
                del bucket[index]
                self._keys.remove(key)
                break
        else:
            raise KeyError(key)

    def __iter__(self):
        yield from self.keys

    def __str__(self):
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}.from_dict({str(self)})'

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, self.__class__):
            return set(self.pairs) == set(other.pairs)
        return False

    def copy(self):
        return HashTable.from_dict(dict(self.pairs), self.capacity)

    def update(self, dictionary: dict = None, **kwargs):
        if not dictionary:
            dictionary = {}
        if kwargs:
            dictionary.update(kwargs)
        if dictionary:
            for key, value in dictionary.items():
                self[key] = value
    
    # def _probe(self, key):
    #     index = self._index(key)
    #     for _ in range(self.capacity):
    #         yield index, self._slots[index]
    #         index = (index + 1) % self.capacity

    @property
    def keys(self):
        return self._keys.copy()

    @property
    def pairs(self):
        return [(key, self[key]) for key in self.keys]

    @property
    def values(self):
        return [self[key] for key in self.keys]


    @property
    def capacity(self):
        return len(self._buckets)

    @property
    def load_factor(self):
        occupied = [bucket for bucket in self._buckets if bucket]
        return len(occupied) / self.capacity

    def _index(self, key):
        return hash(key) % self.capacity

    def _resize_and_rehash(self):
        copy = HashTable(capacity=self.capacity * 2)
        for key, value in self.pairs:
            copy[key] = value
            self._buckets = copy._buckets
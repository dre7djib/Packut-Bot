class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.map = [None] * self.size

    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def insert(self, key, value):
        hash_key = self._get_hash(key)
        self.map[hash_key] = value

    def get(self, key):
        hash_key = self._get_hash(key)
        return self.map[hash_key]

    def remove(self, key):
        hash_key = self._get_hash(key)
        self.map[hash_key] = None

    def get_length(self):
        length = 0
        for item in self.map:
            if item is not None:
                length += 1
        return length

    def get_all(self):
        data_list = []
        for item in self.map:
            if item is not None:
                data_list.append(item)
        return data_list

    def is_empty(self):
        return self.get_length() == 0

    def clear(self):
        self.map = [None] * self.size
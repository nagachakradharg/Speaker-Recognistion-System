from collections.abc import MutableMapping


class Hashtable(MutableMapping):
    """
    Hashtable implemented with seperate chaining

    The __init__ method takes in capacity, default_value, load_factor, growth_factor as instance attributes
    The __setitem__ method to add element
    The __getitem__ method to retrieve element
    The __delitem__ method to remove element
    The __len__ method return the current occupied capacity
    The __iter__ method is there to stisfy the inheritance conditions from MutableMapping

    Atributes:
        capacity (int): initial number of cells to use
        default_value (int): value to return when key is not present
        load_factor (float): to check the occupied capacity
        growth_factor (int): size factor to increase the capacity
    """
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self._items = [None] * capacity
        self.default_value = default_value
        self.capacity = capacity
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self._length = 0

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf

        DO NOT CHANGE THIS FUNCTION
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val

    def __setitem__(self, key, val):
        hash_num = self._hash(key) % self.capacity
        node = self._items[hash_num]

        # If the node already exists, update it's value
        while node:
            if node.key == key:
                node.value = val
                return
            node = node.linked_node

        # add element if it doesn't already exists
        self._items[hash_num] = Node(key, val, self._items[hash_num])
        self._length += 1

        # expand the hashtable if the load factor is reached
        self.expand() if self._length >= self.capacity * self.load_factor else None


    def __getitem__(self, key):
        hash_num = self._hash(key) % self.capacity
        node = self._items[hash_num]

        # is node exists, return it's value
        while node:
            if node.key == key:
                return node.value
            node = node.linked_node

        return self.default_value

    def __delitem__(self, key):
        hash_num = self._hash(key) % self.capacity
        node = self._items[hash_num]

        # delete if the element exists in the hashtable
        if node:
            while node.linked_node:
                if node.linked_node.key == key:
                    node.linked_node = node.linked_node.linked_node
                    self._length -= 1
                    return
                node = node.linked_node

            self._items[hash_num] = self._items[hash_num].linked_node
            self._length -= 1
        else:
            raise KeyError
    
    def __len__(self):
        return self._length

    def __iter__(self):
        raise NotImplementedError("__iter__ not implemented")
    
    def expand(self):
        """
        The function increases the capacity of the hashtable by growth factor times
        when the load factor is reached
        """
        self.capacity = int(self.capacity * self.growth_factor)
        self._length = 0
        current = self._items
        self._items = [None] * self.capacity

        # Filling the elements back to the expanded hashtable
        for node in current:
            while node:
                self[node.key] = node.value
                node = node.linked_node


class Node:
    """
    Mode allows us to implement each link in a linked list

    The __init__ method takes in key, value, and an optional linked_node as instance attributes

    Atributes:
        key (str): initial number of cells to use
        value (int): value to return when key is not present
        linked_node (float): to check the occupied capacity
    """
    def __init__(self, key, value, linked_node=None):
        self.key = key
        self.value = value
        self.linked_node = linked_node
class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.bucket = [None] * capacity #storage
        self.capacity = capacity 


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.bucket)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        load = 0
        for x in self.bucket:
            if x != None:
                load += 1
        load_factor = load / self.capacity
        if load_factor > 0.7:
            self.resize(int(2 * self.capacity))
        elif load_factor < 0.2:
            self.resize(int(self.capacity / 2))
        return load_factor


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        byte_array = key.encode('utf-8')

        for byte in byte_array:
            hash = ((hash * 33) ^ byte) % 0x100000000

        return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def rehash(self, key, value):
        h = self.hash_index(key)
        current_value = self.bucket[h]
        if current_value == None:
            self.bucket[h] = HashTableEntry(key, value)
        else:
            new_entry = HashTableEntry(key, value)
            new_entry.next = current_value
            self.bucket[h] = new_entry        

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        h = self.hash_index(key)
        current_value = self.bucket[h]
        if current_value == None:
            self.bucket[h] = HashTableEntry(key, value)
        else:
            new_entry = HashTableEntry(key, value)
            new_entry.next = current_value
            self.bucket[h] = new_entry
        self.get_load_factor()

        # key_hash = self.djb2(key)
        # bucket_idx = key_hash % self.capacity

        # new = HashTableEntry(key, value)
        # existing = self.bucket[bucket_idx]

        # if existing:
        #     last = None
        #     while existing:
        #         if existing.key == key:
        #             existing.value = value
        #             return
        #         last = existing
        #         existing = existing.next

        #     last.next = new
        # else:
        #     self.bucket[bucket_idx] = new


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        h = self.hash_index(key)
        current_node = self.bucket[h]
        while current_node.next != None:
            if current_node.key == key:
                current_node.value = None
                return
            else:
                current_node = current_node.next
        if current_node.next == None:
            if current_node.key == key:
                current_node.value = None
        self.get_load_factor()

        # key_hash = self.djb2(key)
        # bucket_idx = key_hash % self.capacity

        # existing_value = self.bucket[bucket_idx]
        # if existing_value:
        #     last = None
        #     while existing_value:
        #         if existing_value.key == key:
        #             if last:
        #                 last.next = existing_value.next
        #             else:
        #                 self.bucket[bucket_idx] = existing_value.next
        #         last = existing_value
        #         existing_value = existing_value.next


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        current_node = None
        for x in range(len(self.bucket)):
            current_node = self.bucket[x]
            while current_node != None:
                if current_node.key == key:
                    return current_node.value
                else:
                    current_node = current_node.next

        # key_hash = self.djb2(key)
        # bucket_idx = key_hash % self.capacity

        # existing_value = self.bucket[bucket_idx]
        # if existing_value:
        #     while existing_value:
        #         if existing_value.key == key:
        #             return existing_value.value
        #         existing_value = existing_value.next

        # return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        pairs = {}
        for x in range(len(self.bucket)):
            current_node = self.bucket[x]
            if current_node == None:
                pass
            else:
                if current_node.next == None:
                    pairs[current_node.key] = current_node.value
                while current_node.next != None:
                    pairs[current_node.key] = current_node.value
                    current_node = current_node.next
        self.capacity = new_capacity
        self.bucket = [None] * (self.capacity if self.capacity > 8 else 8)

        for key in pairs:
            self.rehash(key, pairs[key])



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

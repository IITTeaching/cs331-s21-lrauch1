import random
from unittest import TestCase


################################################################################
# Linked list class you should implement
class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next = next

    def __init__(self):
        self.head = LinkedList.Node(None) # sentinel node (never to be removed)
        self.head.prior = self.head.next = self.head # set up "circular" topology
        self.cursor = self.head
        self.length = 0

    ### prepend and append, below, from class discussion

    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1

    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1

    ### subscript-based access ###

    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx

    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        assert(isinstance(idx, int))
        ### BEGIN SOLUTION
        indx = self._normalize_idx(idx)
        if indx >= self.length:
            raise IndexError
        link = self.head.next
        if idx < 0:
            link = self.head.prior
            for i in range(-idx-1):
                link = link.prior
            return link.val
        for i in range(indx):
            link = link.next
        return link.val
        ### END SOLUTION

    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert(isinstance(idx, int))
        indx = self._normalize_idx(idx)
        ### BEGIN SOLUTION
        if indx >= self.length:
            raise IndexError
        link = self.head.next
        for i in range(indx):
            link = link.next
        link.val = value
        ### END SOLUTION

    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert(isinstance(idx, int))
        indx = self._normalize_idx(idx)
        ### BEGIN SOLUTION
        if indx >= self.length:
            raise IndexError
        link = self.head.next
        for i in range(indx):
            link = link.next
        link.prior.next = link.next
        link.prior.next.prior = link.prior
        ### END SOLUTION

    ### cursor-based access ###

    def cursor_get(self):
        """retrieves the value at the current cursor position"""
        assert self.cursor is not self.head
        ### BEGIN SOLUTION
        return self.cursor.val
        ### END SOLUTION

    def cursor_set(self, idx):
        """sets the cursor to the node at the provided index"""
        ### BEGIN SOLUTION
        link = self.head.next
        for i in range(idx):
            link = link.next
        self.cursor = link
        ### END SOLUTION

    def cursor_move(self, offset):
        """moves the cursor forward or backward by the provided offset
        (a positive or negative integer); note that it is possible to advance
        the cursor by further than the length of the list, in which case the
        cursor will just "wrap around" the list, skipping over the sentinel
        node as needed"""
        assert len(self) > 0
        ### BEGIN SOLUTION
        if offset > 0:
            for i in range(offset):
                self.cursor = self.cursor.next
                if self.cursor is self.head:
                    self.cursor = self.cursor.next
            if self.cursor is self.head:
                self.cursor = self.cursor.next
        elif offset < 0:
            num = offset*-1
            for i in range(num):
                self.cursor = self.cursor.prior
                if self.cursor is self.head:
                    self.cursor = self.cursor.prior
            if self.cursor is self.head:
                self.cursor = self.cursor.prior
        ### END SOLUTION

    def cursor_insert(self, value):
        """inserts a new value after the cursor and sets the cursor to the
        new node"""
        ### BEGIN SOLUTION
        link = self.cursor.next
        newlink = LinkedList.Node(value,self.cursor,link)
        self.cursor.next = newlink
        self.cursor = newlink
        link.prior = newlink
        self.length+=1
        ### END SOLUTION

    def cursor_delete(self):
        """deletes the node the cursor refers to and sets the cursor to the
        following node"""
        assert self.cursor is not self.head and len(self) > 0
        ### BEGIN SOLUTION
        self.cursor = self.cursor.next
        if self.cursor is self.head:
            self.cursor = self.cursor.next
            self.cursor.prior.prior.prior.next = self.cursor
            self.cursor.prior = self.cursor.prior.prior.prior
        else:
            self.cursor.prior.prior.next = self.cursor
            self.cursor.prior = self.cursor.prior.prior
        self.length-=1
        ### END SOLUTION

    ### stringification ###

    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        ### BEGIN SOLUTION
        stir = '['
        head = self.cursor
        if self.cursor is self.head:
            head = head.next
        else:
            stir = stir + str(head.val) +', '
            head = head.next

        while not head == self.cursor:
            if head.next == self.cursor:
                stir = stir + str(head.val)
                break
            stir = stir + str(head.val) +', '
            head = head.next
        stir = stir + ']'
        return stir
        ### END SOLUTION

    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        ### BEGIN SOLUTION
        stir = '['
        head = self.cursor
        if self.cursor is self.head:
            head = head.next
        else:
            stir = stir + str(head.val) +', '
            head = head.next

        while not head == self.cursor:
            if head.next == self.cursor:
                stir = stir + str(head.val)
                break
            stir = stir + str(head.val) +', '
            head = head.next
        stir = stir + ']'
        return stir
        ### END SOLUTION

    ### single-element manipulation ###

    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        ### BEGIN SOLUTION
        idx = self._normalize_idx(idx)
        if idx > len(self):
            raise IndexError
        head = self.head.next
        for i in range(idx):
            head = head.next
        head = head.prior
        val = LinkedList.Node(value,head,head.next)
        head.next = val
        val.next.prior = val
        self.length+=1
        ### END SOLUTION

    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        ### BEGIN SOLUTION
        ind = self._normalize_idx(idx)
        head = self.head.next
        for i in range(ind):
            head = head.next
        head = head.prior
        saved = head.next
        head.next = head.next.next
        head.next.prior = head
        self.length-=1
        return saved.val
        ### END SOLUTION

    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        ### BEGIN SOLUTION
        head = self.head.next
        valued = None
        while head is not self.head:
            if value == head.val:
                valued = True
                break
            else:
                head = head.next
        if valued == None:
            raise ValueError
        else:
            head.prior.next = head.next
            head.next.prior = head.prior
        self.length-=1
        
        ### END SOLUTION

    ### predicates (T/F queries) ###

    def __eq__(self, other):
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""
        ### BEGIN SOLUTION
        head = self.head.next
        hed  = other.head.next
        if not head.val == hed.val:
            return False

        while True:
            val = head.val
            v = hed.val
            if val == v:
                head = head.next
                hed = hed.next
            else:
                return False
            if head == self.head or hed == other.head:
                break
        if head == self.head and hed == other.head:
            return True
        else:
            return False
        
        ### END SOLUTION

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        ### BEGIN SOLUTION
        head = self.head.next
        if head.val == value:
            return True

        while True:
            val = head.val
            if val == value:
                return True
            else:
                head = head.next
            if head == self.head:
                break
        return False
        ### END SOLUTION

    ### queries ###

    def __len__(self):
        """Implements `len(self)`"""
        return self.length

    def min(self):
        """Returns the minimum value in this list."""
        ### BEGIN SOLUTION
        head = self.head.next
        val = head.val
        while True:
            head = head.next
            if head == self.head:
                break
            v = head.val
            if v < val:
                val = v
            
        return val
        ### END SOLUTION

    def max(self):
        """Returns the maximum value in this list."""
        ### BEGIN SOLUTION
        head = self.head.next
        val = head.val
        while True:
            head = head.next
            if head == self.head:
                break
            v = head.val
            if v > val:
                val = v
        return val
        ### END SOLUTION

    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        ### BEGIN SOLUTION
        head = self.head.next
        indexed = 0
        i = self._normalize_idx(i)
        for k in range(i):
            head = head.next
            indexed+=1
        if not indexed == i:
            raise IndexError
        if j == None:
            end = len(self)
        else: 
            end = self._normalize_idx(j)
        while not indexed == end:
            if head.val == value:
                return indexed
            else:
                head = head.next
                indexed+=1
        raise ValueError
        ### END SOLUTION

    def count(self, value):
        """Returns the number of times value appears in this list."""
        ### BEGIN SOLUTION
        head = self.head.next
        summat = 0
        while True:
            val = head.val
            if val == value:
                summat+=1
            head = head.next
            if head == self.head:
                break
        return summat
        ### END SOLUTION

    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those
        of other."""
        assert(isinstance(other, LinkedList))
        ### BEGIN SOLUTION
        link = LinkedList()
        head1 = self.head.next
        while not head1 == self.head:
            link.append(head1.val)
            head1 = head1.next
    
        head2 = other.head.next
        while not head2 == other.head:
            link.append(head2.val)
            head2 = head2.next
        return link

        ### END SOLUTION

    def clear(self):
        """Removes all elements from this list."""
        ### BEGIN SOLUTION
        self.head.next = self.head
        self.head.prior = self.head
        self.length=0
        self.cursor = self.head
        ### END SOLUTION

    def copy(self):
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""
        ### BEGIN SOLUTION
        s = LinkedList()
        head = self.head.next
        while True:
            s.append(head.val)
            head = head.next
            if head == self.head:
                break
        return s
        ### END SOLUTION

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        ### BEGIN SOLUTION
        it = iter(other)
        while True:
            try:
                obj = next(it)
                self.append(obj)
            except StopIteration:
                break
        ### END SOLUTION

    ### iteration ###
    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        ### BEGIN SOLUTION
        for i in range(len(self)):
            yield self.__getitem__(i)
        ### END SOLUTION

    ### reverse ###
    def reverse(self):
        """Return a copy of the list with all elements in reverse order.

        E.g., for [1,2,3] you shoudl return [3,2,1].
        """
        ### BEGIN SOLUTION
        s = LinkedList()
        head = self.head.prior
        while True:
            s.append(head.val)
            head = head.prior
            if head == self.head:
                break
        return s
        ### END SOLUTION


################################################################################
# TEST CASES
################################################################################

################################################################################
def say_test(mess):
    print(80 * "*" + "\n" + mess)

def say_success():
    print("SUCCESS")

################################################################################
# (11 points) test subscript-based access
def test_subscript_access():
    say_test("test_subscript_access")
    tc = TestCase()
    data = [1, 2, 3, 4]
    lst = LinkedList()
    for d in data:
        lst.append(d)

    for i in range(len(data)):
        tc.assertEqual(lst[i], data[i])

    with tc.assertRaises(IndexError):
        x = lst[100]

    with tc.assertRaises(IndexError):
        lst[100] = 0

    with tc.assertRaises(IndexError):
        del lst[100]

    lst[1] = data[1] = 20
    del data[0]
    del lst[0]

    for i in range(len(data)):
        tc.assertEqual(lst[i], data[i])

    data = [random.randint(1, 100) for _ in range(100)]
    lst = LinkedList()
    for d in data:
        lst.append(d)

    for i in range(len(data)):
        lst[i] = data[i] = random.randint(101, 200)
    for i in range(50):
        to_del = random.randrange(len(data))
        del lst[to_del]
        del data[to_del]

    for i in range(len(data)):
        tc.assertEqual(lst[i], data[i])

    for i in range(0, -len(data), -1):
        tc.assertEqual(lst[i], data[i])

################################################################################
### (12 points) test cursor-based access
def test_custor_based_access():
    say_test("test_custor_based_access")
    tc = TestCase()

    ## insert a bunch of values at different cursor positions

    lst1 = []
    lst2 = LinkedList()
    for _ in range(100):
        val = random.randrange(1000)
        lst1.append(val)
        lst2.append(val)

    for _ in range(10):
        pos = random.randrange(len(lst1))
        vals = [random.randrange(1000) for _ in range(10)]
        lst1[pos+1:pos+1] = vals
        lst2.cursor_set(pos)
        for x in vals:
            lst2.cursor_insert(x)

    assert len(lst1) == len(lst2)
    for i in range(len(lst1)):
        assert lst1[i] == lst2[i]

    ## move the cursor around and check that values are correct

    lst1 = []
    lst2 = LinkedList()
    for _ in range(100):
        val = random.randrange(1000)
        lst1.append(val)
        lst2.append(val)

    idx = 0
    lst2.cursor_set(0)
    for _ in range(100):
        offset = random.randrange(-200, 200)
        idx = (idx + offset) % 100
        lst2.cursor_move(offset)
        assert lst1[idx] == lst2.cursor_get()

    ## move the cursor around and delete values at the cursor

    lst1 = []
    lst2 = LinkedList()
    for _ in range(500):
        val = random.randrange(1000)
        lst1.append(val)
        lst2.append(val)

    idx = 0
    lst2.cursor_set(0)
    for _ in range(100):
        offset = random.randrange(-200, 200)
        idx = (idx + offset) % len(lst1)
        lst2.cursor_move(offset)
        del lst1[idx]
        lst2.cursor_delete()

    assert len(lst1) == len(lst2)
    for i in range(len(lst1)):
        assert lst1[i] == lst2[i]


################################################################################
# (11 points) test stringification
def test_stringification():
    say_test("test_stringification")
    tc = TestCase()

    lst = LinkedList()
    tc.assertEqual('[]', str(lst))
    tc.assertEqual('[]', repr(lst))

    lst.append(1)
    tc.assertEqual('[1]', str(lst))
    tc.assertEqual('[1]', repr(lst))

    lst = LinkedList()
    for d in (10, 20, 30, 40, 50):
        lst.append(d)
    tc.assertEqual('[10, 20, 30, 40, 50]', str(lst))
    tc.assertEqual('[10, 20, 30, 40, 50]', repr(lst))

################################################################################
# (11 points) test single-element manipulation
def test_single_element_manipulation():
    say_test("test_single_element_manipulation")
    tc = TestCase()
    lst = LinkedList()
    data = []

    for _ in range(100):
        to_ins = random.randrange(1000)
        ins_idx = random.randrange(len(data)+1)
        data.insert(ins_idx, to_ins)
        lst.insert(ins_idx, to_ins)

    for i in range(100):
        tc.assertEqual(data[i], lst[i])

    for _ in range(50):
        pop_idx = random.randrange(len(data))
        tc.assertEqual(data.pop(pop_idx), lst.pop(pop_idx))

    for i in range(50):
        tc.assertEqual(data[i], lst[i])

    for _ in range(25):
        to_rem = data[random.randrange(len(data))]
        data.remove(to_rem)
        lst.remove(to_rem)

    for i in range(25):
        tc.assertEqual(data[i], lst[i])

    with tc.assertRaises(ValueError):
        lst.remove(9999)

################################################################################
# (11 points) test predicates
def test_predicates():
    say_test("test_predicates")
    tc = TestCase()
    lst = LinkedList()
    lst2 = LinkedList()

    tc.assertEqual(lst, lst2)

    lst2.append(100)
    tc.assertNotEqual(lst, lst2)

    lst.append(100)
    tc.assertEqual(lst, lst2)

    tc.assertFalse(1 in lst)
    tc.assertFalse(None in lst)

    lst = LinkedList()
    for i in range(100):
        lst.append(i)
    tc.assertFalse(100 in lst)
    tc.assertTrue(50 in lst)

################################################################################
# (11 points) test queries
def test_queries():
    say_test("test_queries")
    tc = TestCase()
    lst = LinkedList()

    tc.assertEqual(0, len(lst))
    tc.assertEqual(0, lst.count(1))
    with tc.assertRaises(ValueError):
        lst.index(1)

    import random
    data = [random.randrange(1000) for _ in range(100)]
    for d in data:
        lst.append(d)

    tc.assertEqual(100, len(lst))
    tc.assertEqual(min(data), lst.min())
    tc.assertEqual(max(data), lst.max())
    for x in data:
        tc.assertEqual(data.index(x), lst.index(x))
        tc.assertEqual(data.count(x), lst.count(x))

    with tc.assertRaises(ValueError):
        lst.index(1000)

    lst = LinkedList()
    for d in (1, 2, 1, 2, 1, 1, 1, 2, 1):
        lst.append(d)
    tc.assertEqual(1, lst.index(2))
    tc.assertEqual(1, lst.index(2, 1))
    tc.assertEqual(3, lst.index(2, 2))
    tc.assertEqual(7, lst.index(2, 4))
    tc.assertEqual(7, lst.index(2, 4, -1))
    with tc.assertRaises(ValueError):
        lst.index(2, 4, -2)

################################################################################
# (11 points) test bulk operations
def test_bulk_operations():
    say_test("test_bulk_operations")
    tc = TestCase()
    lst = LinkedList()
    lst2 = LinkedList()
    lst3 = lst + lst2

    tc.assertIsInstance(lst3, LinkedList)
    tc.assertEqual(0, len(lst3))

    import random
    data  = [random.randrange(1000) for _ in range(50)]
    data2 = [random.randrange(1000) for _ in range(50)]
    for d in data:
        lst.append(d)
    for d in data2:
        lst2.append(d)
    lst3 = lst + lst2
    tc.assertEqual(100, len(lst3))
    data3 = data + data2
    for i in range(len(data3)):
        tc.assertEqual(data3[i], lst3[i])

    lst.clear()
    tc.assertEqual(0, len(lst))
    with tc.assertRaises(IndexError):
        lst[0]

    for d in data:
        lst.append(d)
    lst2 = lst.copy()
    tc.assertIsNot(lst, lst2)
    tc.assertIsNot(lst.head.next, lst2.head.next)
    for i in range(len(data)):
        tc.assertEqual(lst[i], lst2[i])
    tc.assertEqual(lst, lst2)

    lst.clear()
    lst.extend(range(10))
    lst.extend(range(10,0,-1))
    lst.extend(data.copy())
    tc.assertEqual(70, len(lst))

    data = list(range(10)) + list(range(10, 0, -1)) + data
    for i in range(len(data)):
        tc.assertEqual(data[i], lst[i])

################################################################################
# (11 points) test iteration
def test_iteration():
    say_test("test_iteration")
    tc = TestCase()
    lst = LinkedList()

    import random
    data = [random.randrange(1000) for _ in range(100)]
    lst = LinkedList()
    for d in data:
        lst.append(d)
    tc.assertEqual(data, [x for x in lst])

    it1 = iter(lst)
    it2 = iter(lst)
    for x in data:
        tc.assertEqual(next(it1), x)
        tc.assertEqual(next(it2), x)

################################################################################
# (11 points) test reverse
def test_reverse():
    say_test("test_reverse")
    tc = TestCase()
    lst = LinkedList()

    import random
    data = [random.randrange(1000) for _ in range(20)]
    lst = LinkedList()
    for d in data:
        lst.append(d)

    rev = lst.reverse()
    for i in range(0, len(data)):
        tc.assertEqual(lst[i], rev[len(data) - i - 1])

################################################################################
# MAIN
def main():
    for t in [test_subscript_access,
              test_custor_based_access,
              test_stringification,
              test_single_element_manipulation,
              test_predicates,
              test_queries,
              test_bulk_operations,
              test_iteration,
              test_reverse]:
         t()
         say_success()

if __name__ == '__main__':
    main()

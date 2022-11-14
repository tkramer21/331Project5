"""
CSE331 Project 5 SS'22
Circular Double-Ended Queue
tests.py
"""

import random
import unittest
from solution import CircularDeque, File, filter_corrupted
from xml.dom import minidom

random.seed(1342)

NAMES = ['Jacob', 'H', 'Andrew', 'Ian', 'Onsay', 'Abhinay', 'Brooke', 'Lukas', 'Alex', 'Matt', 'Aaron', 'Adam', 'Joe',
         'Bank', 'Zach']


class CircularDequeTests(unittest.TestCase):
    def test_len(self):
        # Test 1 : length 0
        cd = CircularDeque()
        self.assertEqual(0, len(cd))

        # Test 2 : length 1
        cd = CircularDeque([1])
        self.assertEqual(1, len(cd))

        # Test 3 : length 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, len(cd))

        # Test 4 : length 50
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertEqual(50, len(cd))

    def test_is_empty(self):
        # Test 1 : Empty deque -> true
        cd = CircularDeque()
        self.assertTrue(cd.is_empty())

        # Test 2 : length 1 -> false
        cd = CircularDeque([1])
        self.assertFalse(cd.is_empty())

        # Test 3 : length 2 -> false
        cd = CircularDeque([1, 2])
        self.assertFalse(cd.is_empty())

        # Test 4 : length 50 -> false
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertFalse(cd.is_empty())

    def test_front_element(self):
        # Test 1: Empty deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.front_element())

        # Test 2: CD <1> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.front_element())

        # Test 3: CD <2, 1> -> 2
        cd = CircularDeque([2, 1])
        self.assertEqual(2, cd.front_element())

        # Test 4: CD <50, 49, ..., 0> -> 50
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(50, cd.front_element())

    def test_back_element(self):
        # Test 1: Empty Deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.back_element())

        # Test 2: CD <1> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.back_element())

        # Test 3: CD <1, 2> -> 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, cd.back_element())

        # Test 4: CD <50, 49, ..., 0> -> 0
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(1, cd.back_element())

    def test_grow(self):
        """
        Tests grow functionality without use of enqueue
        Note that we call the grow function directly
        thus if you have a capacity check in your grow function this will fail
        """
        # Test (1) Empty Dequeue
        cd = CircularDeque()
        cd.grow()
        self.assertEqual(0, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual([None] * 8, cd.queue)

        # Test (2) Four element dequeue then grow
        cd = CircularDeque(NAMES[:4])
        cd.grow()
        self.assertEqual(4, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4] + [None] * 4, cd.queue)

    def test_shrink(self):
        """
        Tests shrink without the use of dequeue
        NOTE: If you have a capacity/size check in your shrink this will fail since we call shrink directly
        """

        # Test 1, Capacity 8 -> 4
        cd = CircularDeque(NAMES[:4], capacity=8)
        cd.shrink()
        self.assertEqual(4, cd.capacity)
        self.assertEqual(4, cd.size)

        # Test 2, Capacity 16 -> 8
        cd = CircularDeque(NAMES[:8], capacity=16)
        cd.shrink()
        self.assertEqual(8, cd.capacity)
        self.assertEqual(8, cd.size)

    def test_front_enqueue_basic(self):
        """
        Tests front enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First')
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd.enqueue('Second')
        self.assertEqual(3, cd.front)  # Test 2
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['First', None, None, 'Second'], cd.queue)

        # Set deque capacity to 100, use name list which has length 14 thus we'll
        # never grow with unique insertion because math

        # Test 3: Front enqueue no wrap-around
        cd = CircularDeque(front=50, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual(49 - i, cd.front)
            self.assertEqual('Start', cd.back_element())  # back_element should never change
            self.assertEqual(50, cd.back)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 4: Front enqueue wrap-around
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual((100 - i) % 100, cd.front)
            self.assertEqual('Jacob', cd.back_element())  # back_element should never change
            self.assertEqual(0, cd.back)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_back_enqueue_basic(self):
        """
        Tests back enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First', front=False)
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd = CircularDeque(data=['First'], front=3)
        cd.enqueue('Second', front=False)
        self.assertEqual(3, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['Second', None, None, 'First'], cd.queue)

        # Test 3: Back enqueue normal (no wrap around) more elements
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual(i, cd.back)
            self.assertEqual('Jacob', cd.front_element())  # back_element should never change
            self.assertEqual(0, cd.front)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 4: Back enqueue wraparound (back < front) more elements
        cd = CircularDeque(front=99, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual((100 + i) % 100, cd.back)
            self.assertEqual('Start', cd.front_element())  # front_element should never change
            self.assertEqual(99, cd.front)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_front_enqueue(self):
        """
        Tests front_enqueue and grow functionality
        """
        # Test 1: Front_enqueue, multiple grows with 50 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element)
            # Test capacity of the dequeue while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the dequeue
        self.assertEqual(list(range(32, 0, -1)) + [None] * 14 + list(range(50, 32, -1)), cd.queue)
        self.assertEqual(50, cd.size)

        # Test 2: Front_enqueue, multiple grows with 64 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element)
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the cd
        self.assertEqual(list(range(64, 0, -1)) + [None] * 64, cd.queue)
        self.assertEqual(64, cd.size)
        self.assertEqual(128, cd.capacity)

    def test_back_enqueue(self):
        """
        Tests back_enqueue and grow functionality
        """
        # Test 1: 50 item, multiple grows
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 51)) + [None] * 14, cd.queue)
        self.assertEqual(64, cd.capacity)
        self.assertEqual(50, cd.size)

        # Test 2: 64 items, multiple grows
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 65)) + [None] * 64, cd.queue)
        self.assertEqual(128, cd.capacity)
        self.assertEqual(64, cd.size)

    def test_front_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue())

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue())
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([0, 1, 2])
        for i in range(3):
            self.assertEqual(i, cd.front)
            self.assertEqual(i, cd.dequeue())
            self.assertEqual(2 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [3, 0, 1, 2]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 3
        cd.back = 2
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.front)
            self.assertEqual(dequeue_result[i], cd.dequeue())
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue())

    def test_back_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue(False))

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue(False))
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([3, 2, 1, 0])
        for i in range(4):
            self.assertEqual(3 - i, cd.back)
            self.assertEqual(i, cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [0, 3, 2, 1]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 1
        cd.back = 0
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.back)
            self.assertEqual(dequeue_result[i], cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue(False))

    def test_back_dequeue(self):
        """
        Tests dequeue over shrinking conditions, does test size (length)
        Does not rely on enqueue functions
        """
        # Test 1: Begin with capacity 16, empty queue while checking all parameters
        cd = CircularDeque([i for i in range(15)], capacity=16)

        for item in range(15):
            self.assertEqual(14 - item, cd.dequeue(False))

            if item <= 9:  # shrunk 0 times
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:  # shrunk 1 time
                self.assertEqual(list(range(4)) + [None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:  # shrunk twice
                self.assertEqual([0, 1, None, None], cd.queue)
                self.assertEqual(4, cd.capacity)

            # ensure back is set correctly - note: pointers for an empty queue are up to implementation
            if cd.size != 0:
                self.assertEqual(13 - item, cd.back)

    def test_front_dequeue(self):
        """
        Tests dequeue along with shrinking
        Does not rely on enqueue functions
        """
        # Test 1: identical to above but removing from front rather than back
        cd = CircularDeque([i for i in range(15)], capacity=16)

        fronts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 1, 0, 1]

        for item in range(15):
            self.assertEqual(item, cd.dequeue())

            if item <= 9:
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:
                self.assertEqual([11, 12, 13, 14, None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:
                self.assertEqual([13, 14, None, None], cd.queue)

            if cd.size != 0:
                self.assertEqual(fronts[item], cd.front)

    def test_application(self):
        """
        Tests the application:
        """

        directory = []
        # Test 1
        # Empty list
        self.assertEqual(0, filter_corrupted(directory))  # 0

        # Test 2
        # 1 Element
        # [ A ]
        directory.append(File('A'))
        self.assertEqual(1, filter_corrupted(directory))  # 1

        # Test 3
        # 2 elements
        # [A, B]
        directory.append(File('B'))
        self.assertEqual(2, filter_corrupted(directory))  # 2

        # Test 4
        # Check with 1 duplicate
        # [A, B, A]
        directory.append(File('A'))
        self.assertEqual(2, filter_corrupted(directory))  # 3

        # Test 5
        # Lots of repeating chars
        # [ A, A, A, A, A]
        directory.clear()
        for i in range(5):
            directory.append(File('A'))
        self.assertEqual(1, filter_corrupted(directory))  # 4

        # Test 6
        # List of no repeats
        directory.clear()
        for i in range(25):
            directory.append(File(str(i)))
        self.assertEqual(25, filter_corrupted(directory))  # 5

        # Test 7
        # Some more test
        directory.clear()
        for char in "xkkwfk":
            directory.append(File(char))
        self.assertEqual(3, filter_corrupted(directory))  # 6

        directory.clear()
        for char in "abcabc":
            directory.append(File(char))
        self.assertEqual(3, filter_corrupted(directory))  # 7

        # Test 8
        # Files are case sensitive
        directory.clear()
        for char in "TtEeAaMm":
            directory.append(File(char))
        self.assertEqual(8, filter_corrupted(directory))  # 8


if __name__ == '__main__':
    unittest.main()

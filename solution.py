"""
CSE331 Project 5 FS'22
Circular Double-Ended Queue
solution.py
"""
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# from matplotlib import pyplot as plt  # COMMENT OUT THIS LINE (and `plot_speed`) if you dont want matplotlib
import gc

T = TypeVar('T')


class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            data = ['Start']  # front will get set to 0 by a front enqueue if the initial data is empty
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    #
    # Your code goes here!
    #
    def __len__(self) -> int:
        """
        Determines the length of the queue from front to back
        :return: an int --> the length of the queue
        """
        if self.front is not None:
            return (self.back - self.front) % self.capacity + 1
        else:
            return 0

    def is_empty(self) -> bool:
        """
        Checks to see if the Queue is empty
        :return: A boolean --> True is empty; False otherwise
        """
        if self.front is None:
            return True
        else:
            return False

    def front_element(self) -> T:
        """
        Determines the front element of the Queue
        :return: an object that is pointed to by the front pointer
        """
        if self.front is not None:
            return self.queue[self.front]

    def back_element(self) -> T:
        """
        Determines the back element of the Queue
        :return: an object that is pointed to by the back pointer
        """
        if self.back is not None:
            return self.queue[self.back]

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Adds an object to the front or back of the queue dependent on boolean param
        :param value: the value to be added to the front/back of queue
        :param front: A boolean determining whether obj is added to the front or back of queue
        :return: None
        """
        if not self.is_empty():
            if front is True:
                self.queue[self.front - 1] = value
                self.front -= 1

            else:
                self.queue[self.back + 1 - len(self.queue)] = value
                if self.back == len(self.queue) - 1:
                    self.back = self.back + 1 - len(self.queue)
                else:
                    self.back = self.back + 1

        else:
            self.queue[0] = value
            self.front = 0
            self.back = 0

        self.size += 1
        if self.front < 0:
            self.front = self.front + len(self.queue)

        if self.size == self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Removes an element from the queue by altering the front and back pointers; dependent on boolean param
        :param front: boolean determining whether element is removed from front or back of queue
        :return: the removed element
        """
        if not self.is_empty():
            if front is True:
                removed = self.queue[self.front]
                self.front += 1

            else:
                removed = self.queue[self.back]
                if self.back == 0:
                    self.back = len(self.queue) - 1
                else:
                    self.back -= 1

            self.size -= 1
            if self.size == 0:
                self.front = None
                self.back = None
                return removed

            if self.front == len(self.queue):
                self.front = 0

            if self.size <= (self.capacity // 4) and (self.capacity // 2) >= 4:
                self.shrink()

            return removed

        return None

    def grow(self) -> None:
        """
        Called by enqueue when the circular queue reaches the capacity. Will also reorder the values so that the front
        will be located at index 0
        :return: None
        """
        new = [None] * (len(self.queue) * 2)
        ptr = self.front
        i = 0
        if self.front is not None:
            while i < len(self.queue):
                new[i] = self.queue[ptr]
                if ptr == len(self.queue) - 1:
                    ptr = 0
                else:
                    ptr += 1
                i += 1

            self.front = 0
            self.back = self.size - 1  # check placement/order if having problems with later tests

        self.queue = new
        self.capacity = len(self.queue)

    def shrink(self) -> None:
        """
        Called by dequeue when the circular queue reaches a specific fraction of the capacity.
        Will also reorder the values so that the front will be located at index 0. Will not decrease capacity below 4
        :return: None
        """
        new = [None] * (len(self.queue) // 2)
        ptr = 0  # ptr to insertion in new
        i = 0
        if self.front is not None:
            while i < len(self.queue) and ptr < len(new):
                if self.back > self.front:  # no wrap-around
                    if i >= self.front and i <= self.back:
                        new[ptr] = self.queue[i]
                        ptr += 1
                    else:
                        new[ptr] = None
                elif self.back < self.front:  # wrap-around case
                    if i <= self.front and i >= self.back:
                        new[ptr] = self.queue[i]
                        ptr += 1
                    else:
                        new[ptr] = None
                i += 1

            self.front = 0
            self.back = self.size - 1  # check placement/order if having problems with later tests

        self.queue = new
        self.capacity = len(self.queue)


class File:
    """
    File class stores data, used in application problem
    """

    def __init__(self, data: str) -> None:
        """
        Creates a file with data value
        :param : data , data to be stored in file
        :returns : None
        """
        self.data = data

    def __eq__(self, other: 'File') -> bool:
        """
        Compares two Files by data
        :param other: the other file
        :return: true if comparison is true, else false
        """
        return self.data == other.data

    def __str__(self) -> str:
        """
        :return: a string representation of the File
        """
        return f'File: {self.data}'

    __repr__ = __str__


def filter_corrupted(directory: List[File]) -> int:
    """
    Searches through the list to determine the longest substring without repeating characters. Utilizes dictionary
    :param directory: the list to be searched
    :return: the length of the longest substring without repeats
    """
    key_dict = {}
    max = 0
    counter = 0
    for i in directory:
        if i.data not in key_dict.keys():
            counter += 1
            key_dict[i.data] = True

        elif max < counter:
            max = counter
            counter = 0
            key_dict = {}

        else:
            counter = 0
            key_dict = {}

    if counter > max:
        max = counter

    return max

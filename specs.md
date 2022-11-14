Project 5: Circular Double-Ended Queues (Deque)
===============================================

**Due: Wednesday, October 19th @ 10:00pm pm EST**

_This is not a team project, do not copy someone else’s work._

_![CircularDeque.png](img/CircularDeque.png)_

Assignment Overview
-------------------

In a typical FIFO (First in First out) queue, elements are added to one end of the underlying structure and removed from the opposite. These are natural for storing sequences of instructions: Imagine that instructions are added to the queue when first processed, and removed when completed. The first instruction processed will also be the first completed - we add it to the front, and remove it from the back.

A deque is a [double-ended queue](https://en.wikipedia.org/wiki/Double-ended_queue), meaning elements can be added or removed from either end of the queue. This generalizes the behavior described above to account for more complex usage scenarios. The ability to add or remove from both ends of the deque allows the structure to be used as both a **FIFO queue and a LIFO stack**, simultaneously.

This structure is useful for storing undo operations, where more recent undos are pushed and popped from the top of the deque and old/expired undo are removed from the back of the deque. Trains, consisting of sequences of cars, can also be thought of as deques: cars can be added or removed from either end, but never the middle.

A circular queue is a queue of fixed size with end-to-end connections. This is a way to save memory as deleted elements in the queue can simply be overwritten. In the picture above at index 0, element 1 has been removed (dequeued) from the queue but the value remains. If two new values are enqueued, then that 1 will be overwritten. After this, the circular queue will have reached capacity, and needs to grow.

Circular queues are useful in situations with limited memory. Consider a router in an internet network. A package (a set of bits sent across the network) is sent to this router and it joins the router's processing queue. This router can only hold so many packets before it has to start dropping some. A circular queue would be useful here, as it optimizes memory usage.

A circular deque is a combination of a deque and a circular queue. It sets a max size and can grow and shrink like a circular queue, and it can enqueue/dequeue from both ends.


# Assignment Notes
1. **Manual grading is  30% of the points on this project. Submitted program is checked for its run time for all its functions and space complexity for its add, remove, and the application problem. Space complexity is only required for each project's add, remove and application problem. For these functions where the space complexity is checked, manual grade is splitted 50-50 for run time and space complexity.Be sure to review the rubric and adhere to complexity requirements!**
 Stacks and Queue ADTs  add, remove methods by design already allocate O(N) space. 
2. Docstrings (the multi-line comments beneath each function header) are NOT provided and will need to be completed for full credit.
3. Testcases are your friend: before asking about the form of input/output or what happens in a particular edge case, check to see if the testcases answer your question for you. By showing the expected output in response to each input, they supplement the specs provided here.
4. Don't be afraid to go to D2L Course Tools for tutorial videos on how to debug,  it will help you figure out where you're going wrong far more quickly than ad-hoc print statements!


# Tips

*   The use of [modulo (%)](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations) is highly recommended
*   Understand what [amortized runtime](https://medium.com/@satorusasozaki/amortized-time-in-the-time-complexity-of-an-algorithm-6dd9a5d38045) is (also explained below)
*   Enqueue and Dequeue both have basic tests which test their functionality in conditions where shrink and grow will not be called. This allows you to test your enqueue and dequeue functions without having to implement grow/shrink.
*   Although the API lists enqueue/dequeue first, **it is common to implement grow/shrink and then enqueue/dequeue or grow->enqueue then shrink->dequeue**. The test cases are designed to allow you to implement these functions independently in the order which best suits you.

# Rules:

*   The use of Python's Queues library is **NOT ALLOWED** and any use of it will result in a 0 on this project
*   The use of .pop() is **PROHIBITED.**
    *   Any function using .pop() will be deducted all points for test cases and manual grading
    *   .pop(x) has a runtime of _O(n-x)_, where _n_ is the length of the python list .pop(x) is called on - in most situations, this will violate time complexity. 
*   Changing function signatures is not allowed and will result in all points lost for that particular function.
*   Docstrings (the multi-line comments beneath each function header) are NOT provided and will need to be completed for full credit..
*   Use of the **nonlocal** keyword will result in a 0 on the function is used on
    *   You should never need to use this keyword in this project and if you are using it in a function in this class, you're doing something wrong.



# Assignment Specifications
-------------------------

"There's a term for people who don't read the project details : unemployed" -Dr. Owen.



#### class CircularDeque:

_DO NOT MODIFY the following attributes/functions_

*   **Attributes**
    *   **capacity: int:** the total amount of items that can be placed in your circular deque. capacity grows and shrinks dynamically, but the capacity is never less than 4. It will always be greater than or equal to **size**.
    *   **size: int:** the number of items currently in your circular deque
    *   **queue: list\[T\]:** The underlying structure holding the data of your circular deque. Many elements may be **None** if your current **size** is less than **capacity**. This grows and shrinks dynamically.
    *   **front: int:** an index indicating the location of the first element in the circular deque
    *   **back: int:** an index indicating the location of the last element in your circular deque
*   **\_\_init\_\_(self, data: list\[T\], front: int, capacity: int) -> None**
    *   Constructs a circular deque
    *   **data: list\[T\]:** a list containing all data to be inserted into the circular deque
    *   **front: int:** An index to offset the front pointer to test the circular behavior of the list without growing
    *   **capacity: int:** the capacity of the circular deque
    *   **Returns:** None
*   **\_\_str\_\_(self) -> str** and **\_\_repr\_\_(self) -> str**
    *   Represents the circular deque as a string
    *   **Returns:** str

_IMPLEMENT the following functions_

*   **\_\_len\_\_(self) -> int**
    *   Returns the length/size of the circular deque - this is the number of items currently in the circular deque, and will not necessarily be equal to the **capacity**
    *   This is a [magic method](https://www.tutorialsteacher.com/python/magic-methods-in-python) and can be called with **len(object\_to\_measure)**
    *   Time complexity: _O(1)_
    *   **Returns:** int representing length of the circular deque
*   **is\_empty(self) -> bool**  
    *   Returns a boolean indicating if the circular deque is empty
    *   Time complexity: _O(1)_
    *   **Returns:** True if empty, False otherwise
*   **front\_element(self) -> T**  
    *   Returns the first element in the circular deque
    *   Time complexity: _O(1)_

    *   **Returns:** the first element if it exists, otherwise None
*   **back\_element(self) -> T**  
    *   Returns the last element in the circular deque
    *   Time complexity: _O(1)_
    *   **Returns:** the last element if it exists, otherwise None
*   **enqueue(self, value: T, front: bool = True) -> None:**  
    *   Add a value to either the front or back of the circular deque based off the parameter **front**
    *   if front is true, add the value to the front. Otherwise, add it to the back
    *   Call **grow()** if the size of the list has reached capacity
    *   **param value: T:** value to add into the circular deque
    *   **param value front:** where to add value T
    *   Time complexity: _O(1)\*_
    *   Space complexity:  _O(N)(due to grow)
 
    *   **Returns:** None
*   **dequeue(self, front: bool = True) -> T:**  
    *   Remove an item from the queue
    *   Removes the front item by default, remove the back item if False is passed in
    *   Calls **shrink()** If the current size is less than or equal to 1/4 the current capacity, and 1/2 the current capacity is greater than or equal to 4, halves the capacity.
    *   **param front:** Whether to remove the front or back item from the dequeue
    *   Hint: You shouldn't delete the value from the dequeue (by setting it to None) as that spot will merely be overwritten when you enqueue on that spot so it's more efficient to only adjust the back/front pointer instead.
    *   Time complexity: _O(1)\*_
    *   Space complexity:  _O(N) (due to shrink)
    *   **Returns:** removed item, None if empty
*   **grow(self) -> None**
    *   Doubles the capacity of CD by creating a new underlying python list with double the capacity of the old one and copies the values over from the current list.
    *   The new copied list will be 'unrolled' s.t. the front element will be at index 0 and the tail element will be at index \[size - 1\]. 
    *   Time complexity: _O(N)_
    *   Space complexity: _O(N)_
    *   **Returns:** None
*   **shrink(self) -> None**
    *   Cuts the capacity of the queue in half using the same idea as grow. Copy over contents of the old list to a new list with half the capacity.
    *   The new copied list will be 'unrolled' s.t. the front element will be at index 0 and the tail element will be at index \[size - 1\]. 
    *   Will never have a capacity lower than 4, **DO NOT** shrink when shrinking would result in a capacity < 4
    *   Time complexity: _O(N)_
    *   Space complexity: _O(N)_
    *   **Returns:** None

\***[Amortized](https://medium.com/@satorusasozaki/amortized-time-in-the-time-complexity-of-an-algorithm-6dd9a5d38045)**. _Amortized Time Complexity_ means 'the time complexity a majority of the time'. Suppose a function has amortized time complexity _O(f(n))_ - this implies that the majority of the time the function falls into the complexity class _O(f(n)),_ however, there may exist situations where the complexity exceeds _O(f(n))._ The same logic defines the concept of _Amortized Space Complexity_.

Example:  enqueue(self, value: T, front: bool)has an amortized time complexity of _O(1)_: In the majority of situations, enqueueing an element occurs through a constant number of operations. However, when the Circular Deque is at capacity, grow(self) is called - this is an _O(n)_ operation, therefore in this particular scenario, enqueue exceeds its amortized bound.

\[//\]: # (application problem)

### Uncorrupt the System!! Overview:

![hacker.jpg](img/hacker.png)

Oh no! You wake up one morning only to find out that someone has corrupted your company’s file system. The hacker has made copies of random files and distributed it throughout the system. Your manager needs you to take the front seat and reverse engineer the hacker’s algorithm.

After taking a closer look at the issue you found a way to save your system and delete the corrupted data. All you have to do now is to find the largest contiguous block of files without any repeats in every directory. Create an algorithm that takes a directory, a list of files and returns the size of uncorrupted data.

### **Expectations**:

You are given the class described below. **DO NOT** modify the class - any modification will result in a zero for this portion of the project.

**class File**

_DO NOT MODIFY the following attributes/functions_

*   **Attributes:**
    *   **data: str:** Data to be stored in a file
*   **\_\_init\_\_(self, data:str) -> None**
    *   Constructs a **File** with data value
    *   **param data:** Data to be stored in a file
    *   **return: None**
*   **\_\_eq\_\_(self, other: File) -> bool**
    *   Compares two **File** objects by value
    *   **param other: CDLLNode:** The other file
    *   **return:** True if the comparison is true, else false
*   **\_\_str\_\_(self) -> str**
    *   returns a string representation of the **File**
    *   **return:** a string

Your mission is to utilize the functionality of your **CircularDeque** with a **File** as the underlying structure.

**You are required to implement the following function:**

*   **filter\_corrupted(directory : List\[File\]) -> int**
    * Uncorrupt the data by finding the largest list of files without any repeats
    * Note: The use of a dictionary or set is allowed in the function
    * **param directory: List\[File\]:** directory list of files to be looked through
    * **Time complexity:** _O(n)_
    * **Space complexity:** _O(n)_
    * **return:** Return the size of the largest list of files without repeats

### **Examples**:

**Example 1:** Directory is empty. Thus, the function returns 0.

**Example 2:** Directory: File A, File B, File C, File A, File D. The longest list of files without an repeats is File A -> File B -> File C. So, the function returns 4.

**Example 3:** Directory: File A, File B, File C, File a, File D. The longest list of files without an repeats is File A -> File B -> File C -> File a -> File D. So, the function returns 5 since the directory is case-sensitive.



## **Submission**


#### **Deliverables**
In every project you will be given a file named as "**solution.py**". Your will work on this file to write your Python code.
We recommend that you **download your "solution.py" and "tests.py" to your local drive**, and work on your project using PyCharm so you can easily debug your code.

Below are the simple steps to work on any project locally in your personal computer in this class:

**APPROACH 1: USING D2L TO DOWNLOAD PROJECT'S STARTER PACKAGE:**
1. Make sure you installed PyCharm
2. You can download the starter package from D2L under Projects content. Watch the short tutorial video on how to download the starter package from D2L and open it up in PyCharm.
3. Work on your project as long as you want then upload your solution.py , (watch the short tutorial video on D2L for uploading your solution.py), and upload your solution.py to Codio.
4. Click Submit button on Guide when you are done!
   ![](img/Submit.png)

**APPROACH 2: USING CODIO TO DOWNLOAD solution.py and tests.py**
1. On your own computer make sure to create a local folder in your local drive, name it something like **ProjectXX**, replace xx with the actual project number, in this case your folder name would be **Project03**.
2. **Download** solution.py from Codio by simply right mouse clicking on the file tree, see image below
   ![](img/Codio_FileTree.png)
3. **Download** tests.py from Codio by simply right mouse clicking on the file tree as shown above.
4. Work locally using PyCharm as long as you need.
5. When finished with your solution.py file, upload your file to Codio by right mouse clicking on the Project Directory on file tree.You should rename or remove the solution.py file that is currently existing in Codio before you upload your completed version.
6. Go To Guide and click Submit button
   ![](img/Codio_Upload.png)


**It does not matter which approach you choose to work on your project, just be sure to upload your solution, “solution.py”, to Codio by and click on the Submit button by its deadline.**
Working locally is recommended so you can learn debugging. You can complete your entire solution.py using Codio editor, debugging may not be as intuitive as PyCharm IDE. For this reason we recommend that you work locally as long as you need, then upload your code to Codio.


**Grading**
The following 100-point rubric will be used to determine your grade on Project5:

*   Tests (70)  
    *   00 - len(): \_\_/2
    *   01 - is\_empty: \_\_/2
    *   02 - front\_element: \_\_/2
    *   03 - back\_element: \_\_/2
    *   04 - front\_enqueue\_basic: \_\_/3
    *   05 - back\_enqueue\_basic: \_\_/3
    *   06 - front\_enqueue: \_\_/7
    *   07 - back\_enqueue: \_\_/7
    *   08 - front\_dequeue\_basic: \_\_/3
    *   09 - back\_dequeue\_basic: \_\_/3
    *   10 - front\_dequeue: \_\_/7
    *   11 - back\_dequeue: \_\_/7
    *   12 - grow: \_\_/5
    *   13 - shrink: \_\_/5
    *   14 - Application: \_\_/12
*   Manual (30)
    *   M0 - len(): \_\_/1           
    *   M1 - is\_empty: \_\_/1
    *   M2 - front\_element: \_\_/2
    *   M3 - back\_element: \_\_/2
    *   M4 - front\_enqueue: \_\_/3  ( run time and space complexity checked)
    *   M5 - back\_enqueue: \_\_/3   ( run time and space complexity checked)
    *   M6 - front\_dequeue: \_\_/2  ( run time and space complexity checked)
    *   M7 - back\_dequeue: \_\_/2   ( run time and space complexity checked)
    *   M8 - grow: \_\_/3            ( run time and space complexity checked)
    *   M9 - shrink: \_\_/3          ( run time and space complexity checked)
    *   M10 - application: \_\_/6    ( run time and space complexity checked)
    *   M11 - feedback & citation: \_\_/2


* **Manual (30 points)**
  * Time complexity must be met for each function. 
  *Time and Space complexity of on add, remove and application problem and points are **divided equally** for each function. If you fail to meet time **or** space complexity in a given function, you receive half of the manual points for that function.
  * Loss of 1 point per missing docstring (max 5 point loss)
  * Loss of 2 points per changed function signature (max 20 point loss)
  * Loss of complexity and loss of testcase points for the required functions in this project. You may not use any additional data structures such as dictionaries, and sets!”
  *   You must actually use the underlying **File** in the provided skeleton for the application problem. The testcases check for this, but attempting to get around the checks will result in a zero.
  * 2 pts  for feedback and citation. See text box below to complete.
* **Important reminder**
  Note students can not use Chegg or similar sites, see syllabus for details, use of outside resources for the application problem is strictly forbidden, use of outside resources is limited to max of 2 functions in a project.


    * **DOCSTRING** is not provided for this project. Please use Project 1 as a template for your DOCSTRING . 
    To learn more on what is a DOCSTRING visit the following website: [What is Docstring?](https://peps.python.org/pep-0257/)
      * One point per function that misses DOCSTRING.
      * Up to 5 points of deductions

This project was created by Khushi Vora and Matt Kight_, contributions from Jacob Caurdy and Andrew Haas_



<input type="checkbox"> <b>STEP 1 :Rename the old solution file by clicking Rename button below. This button renames your file to **solution_old.py** </b>
{Rename}(mv solution.py solution_old.py)

<input type="checkbox"> <b>STEP 2 : Upload your **solution.py** from your computer to Codio File Tree on the left. </b>

<input type="checkbox"> <b>STEP 3: Test your code, by clicking the RUN ALL TESTS button:</b>
{RUN ALL THE TESTS|assessment}(test-262103911)
When you are done running all the test, use the Submit button below to submit your work.

<input type="checkbox"> <b>STEP 4:Submit your code:</b>
{SUBMIT!|assessment}(test-3379255259)
Please note that there will be manual grading after you submit your work. Manual Grading is 30 points in this project. (28 pts for Run Time and Space complexity, +2 points for filling out the feedback and the citation text box)


{Check It!|assessment}(grade-book-3266829715)
{Submit Answer!|assessment}(free-text-3024451938)











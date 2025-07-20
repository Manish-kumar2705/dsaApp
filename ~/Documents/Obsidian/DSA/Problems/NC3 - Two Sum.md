**Two Sum (NC3)**
=====================

**Problem Summary**
---------------

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.

**Brute Force Approach**
---------------------

### Code
```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
### Complexity
* Time complexity: O(n^2), where n is the length of the input array `nums`. This is because we have two nested loops that iterate over the array.
* Space complexity: O(1), since we only use a constant amount of space to store the indices.

**Optimal Approach**
-------------------

### Code
```python
def twoSum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
```
### Complexity
* Time complexity: O(n), where n is the length of the input array `nums`. This is because we only iterate over the array once.
* Space complexity: O(n), since we use a dictionary to store the indices of the numbers.

**Key Insights and Pattern Identification**
-----------------------------------------

* The problem can be solved by using a dictionary to store the indices of the numbers and their complements.
* The optimal approach takes advantage of the fact that we can look up the complement of a number in O(1) time using a dictionary.

**Edge Cases**
-------------

* The input array `nums` is empty.
* The input array `nums` has only one element.
* The `target` is not the sum of any two numbers in the input array.

**Anki Flashcards**
-----------------

### Card 1
Q: What is the time complexity of the brute force approach?
A: O(n^2)

### Card 2
Q: What is the space complexity of the optimal approach?
A: O(n)

### Card 3
Q: What data structure is used in the optimal approach?
A: Dictionary (or Hash Table)

### Card 4
Q: What is the key insight behind the optimal approach?
A: Using a dictionary to store the indices of the numbers and their complements.

### Card 5
Q: What is the edge case where the input array has only one element?
A: In this case, we cannot find two numbers that add up to the target, so we return an empty list.
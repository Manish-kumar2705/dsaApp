**Letter Combinations of a Phone Number (NC78)**
==============================================

**Problem Summary**
---------------

Given a string containing digits from 2-9, return all possible letter combinations that the number could represent. A mapping of digits to letters is provided, where each digit corresponds to a set of letters.

**Brute Force Approach**
---------------------

The brute force approach involves generating all possible combinations of letters for each digit and then combining them to form the final result.

**Code**
```python
def letterCombinations(digits):
    if not digits:
        return []
    
    phone = {
        '2': ['a', 'b', 'c'],
        '3': ['d', 'e', 'f'],
        '4': ['g', 'h', 'i'],
        '5': ['j', 'k', 'l'],
        '6': ['m', 'n', 'o'],
        '7': ['p', 'q', 'r', 's'],
        '8': ['t', 'u', 'v'],
        '9': ['w', 'x', 'y', 'z']
    }
    
    def backtrack(combination, next_digits):
        if len(next_digits) == 0:
            output.append(combination)
        else:
            for letter in phone[next_digits[0]]:
                backtrack(combination + letter, next_digits[1:])
    
    output = []
    backtrack("", digits)
    return output
```

**Complexity**
O(3^n \* 4^m), where n is the number of digits that maps to 3 letters and m is the number of digits that maps to 4 letters.

**Optimal Approach**
-------------------

The optimal approach is similar to the brute force approach, but it uses a more efficient way to generate the combinations.

**Code**
```python
def letterCombinations(digits):
    if not digits:
        return []
    
    phone = {
        '2': ['a', 'b', 'c'],
        '3': ['d', 'e', 'f'],
        '4': ['g', 'h', 'i'],
        '5': ['j', 'k', 'l'],
        '6': ['m', 'n', 'o'],
        '7': ['p', 'q', 'r', 's'],
        '8': ['t', 'u', 'v'],
        '9': ['w', 'x', 'y', 'z']
    }
    
    def backtrack(combination, next_digits):
        if len(next_digits) == 0:
            output.append(combination)
        else:
            for letter in phone[next_digits[0]]:
                backtrack(combination + letter, next_digits[1:])
    
    output = []
    backtrack("", digits)
    return output
```

**Complexity**
O(3^n \* 4^m), where n is the number of digits that maps to 3 letters and m is the number of digits that maps to 4 letters.

**Key Insights and Pattern Identification**
-----------------------------------------

* The problem can be solved using a backtracking approach, where we generate all possible combinations of letters for each digit and then combine them to form the final result.
* The key insight is to identify the pattern of generating combinations for each digit and combining them to form the final result.

**Edge Cases**
-------------

* If the input string is empty, return an empty list.
* If the input string contains digits that are not in the phone mapping, return an empty list.

**Anki Flashcards**
-------------------

### Card 1
Q: What is the problem statement of Letter Combinations of a Phone Number?
A: Given a string containing digits from 2-9, return all possible letter combinations that the number could represent.

### Card 2
Q: What is the brute force approach to solve the problem?
A: Generate all possible combinations of letters for each digit and then combine them to form the final result.

### Card 3
Q: What is the time complexity of the optimal approach?
A: O(3^n \* 4^m), where n is the number of digits that maps to 3 letters and m is the number of digits that maps to 4 letters.

### Card 4
Q: What is the key insight to solve the problem?
A: Identify the pattern of generating combinations for each digit and combining them to form the final result.

### Card 5
Q: What is the edge case when the input string is empty?
A: Return an empty list.
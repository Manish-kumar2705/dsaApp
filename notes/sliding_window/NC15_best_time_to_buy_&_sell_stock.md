Here are the detailed DSA notes for the LeetCode problem: Best Time to Buy & Sell Stock (Pattern: Sliding Window):

## Problem Statement and Examples
Say you have an array `prices` for which the `i-th` element is the price of a given stock on the `i-th` day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. You want to find the maximum possible profit.

**Examples:**

* `prices = [7,1,5,3,6,4]`, Output: `5` (Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5)
* `prices = [7,6,4,3,1]`, Output: `0` (No profit can be made)
* `prices = [1,2,3,4,5]`, Output: `4` (Buy on day 0 (price = 1) and sell on day 4 (price = 5), profit = 5-1 = 4)

## Hints
1. **Think about the minimum price**: To maximize profit, you need to find the minimum price to buy the stock.
2. **Think about the maximum profit**: After finding the minimum price, think about how to find the maximum profit by selling the stock at a higher price.
3. **Use a single pass**: Can you find the maximum profit in a single pass through the array?

## Intuition
The core idea is to keep track of the minimum price seen so far and the maximum profit that can be made. As we iterate through the array, we update the minimum price and maximum profit accordingly.

## General Solution for Pattern
The Sliding Window pattern is used when we need to find a subset of elements in an array that satisfy certain conditions. In this problem, our sliding window is the range of days we consider for buying and selling the stock. We slide this window through the array, updating our minimum price and maximum profit as we go.

Common use cases for the Sliding Window pattern include:

* Finding the maximum sum of a subarray
* Finding the longest substring with a certain property
* Finding the maximum profit in a sequence of prices

## Brute-Force Approach
The brute-force approach would be to consider every possible pair of buy and sell days and calculate the profit for each pair. This would result in a time complexity of O(n^2), where n is the number of days.

**Step-by-step brute force solution:**

1. Iterate through the array with two nested loops, considering every possible pair of buy and sell days.
2. For each pair, calculate the profit by subtracting the buy price from the sell price.
3. Keep track of the maximum profit found.

**Complexity analysis:**

* Time complexity: O(n^2)
* Space complexity: O(1)

## Optimal Solution Breakdown
The optimal solution uses a single pass through the array, keeping track of the minimum price and maximum profit.

**Time complexity:** O(n)
**Space complexity:** O(1)

**Edge cases:**

* If the input array is empty, return 0.
* If the input array has only one element, return 0.

**Optimizations:**

* We only need to keep track of the minimum price and maximum profit, so we don't need to store the entire array.
* We can update the minimum price and maximum profit in a single pass through the array.

## Code (Java)
```java
public int maxProfit(int[] prices) {
    if (prices == null || prices.length == 0) {
        return 0; // edge case: empty array
    }

    int minPrice = prices[0]; // initialize minimum price
    int maxProfit = 0; // initialize maximum profit

    for (int i = 1; i < prices.length; i++) {
        if (prices[i] < minPrice) {
            minPrice = prices[i]; // update minimum price
        } else if (prices[i] - minPrice > maxProfit) {
            maxProfit = prices[i] - minPrice; // update maximum profit
        }
    }

    return maxProfit;
}
```
Note: The code is written in Java, but the approach can be applied to other programming languages as well.
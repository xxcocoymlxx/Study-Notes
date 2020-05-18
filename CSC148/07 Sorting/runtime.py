VIDEO:
https://www.youtube.com/watch?v=6Ol2JbwoJp0

NOTES ON THE PDF:
def max_segment_sum(L):
  '''(list of int) -> int
  Return maximum segment sum of L.
  '''
  max_so_far = 0
  for lower in range(len(L)):
    for upper in range(lower, len(L)):
      sum = 0
      for i in range(lower, upper + 1):
        sum = sum + L[i]
      max_so_far = max(max_so_far, sum)
  return max_so_far


What is the running time of this algorithm? We want an answer in terms of n, not clock time

I want you to find the statement that executes most often; count the number of times that it runs
Statement that runs most often is one in the inner-most loop.
sum = sum + L[i]
Now let's upper-bound the number of times that this statement runs
lower loop runs n times.
Upper loop runs at most n times for each iteration of the lower loop
i loop runs at most n iterations for each iteration of the upper loop.

Now we can upper-bound the total number of times that the inner-most statement runs.
At most n*n*n = n^3
So we have an n^3 algorithm.

More precise: 2+2n^2+n^3 steps

Is it worth it? Or should we just stick to n^3

Prove that 2+2n^2+n^3 is O(n^3).
This means that we have to show 2+2n^2+n^3 is eventually <= kn^3 for some k > 0.

2+2n^2+n^3
<= 2n^3+2n^2+n^3
= 3n^3+2n^2
<= 3n^3+2n^3
= 5n^3

This is our proof that 2+2n^2+n^3 is O(n^3).

----------

We know that the segment-sum code is O(n^3).
Is the code O(n^4) too? Yes
Is it O(n^5)? Yes
Is it O(2^n)? yes
Is it O(n^2)? No

Big oh is an upper bound. If you make it worse (e.g. n^3 to n^4), it's just a worse upper bound. Still technically correct though.

But I want the most accurate bound; lowest upper bound.

----------

I'd like the big oh runtime for the following function.
O(1), O(log n), O(n), O(n log n), O(n^2), O(n^3), ... O(2^n)...
-I want the worst-case upper bound


def bigoh1(n):
  sum = 0
  for i in range(100, n):
    sum = sum+1

  print(sum)


It's O(n). It takes something like n-100 steps, which you can prove is O(n)!

----------

Let's do an ordering of best (fastest) to worst (slowest) algorithm efficiencies:
The best one is O(1). Constant-time algorithm
No matter how big your input, your runtime does not increase.
Example:
def f(n):
  print('hello world')

-Return the first element of a list.
-Return the maximum of two characters.


Between constant and linear is O(log n)
Example: binary search


Getting worse...
O(n), linear algorithm.
-Printing all elements in a list
-finding the maximum element in a list

A little bit worse is O(n log n)
Examples: quicksort (on average), mergesort

Slower is O(n^2): bubble sort, insertion sort, selection sort

Slower is O(n^3): maximum segment sum code

Slower is O(n^4), O(n^5)...

...

Eventually you get so bad that you can't even use them in practice
O(2^n). As n increases by 1, you double the amount of time you take

Even worse...
O(n!). Like the permutation approach to finding all anagrams

O(n^n)

Huge difference between O(n^k) polynomials and O(k^n) exponential functions.
O(n^2) and O(2^n): very different. 
O(n^2)is computable for reasonable-sized input; O(2^n) is not.

----------

I'd like the big oh runtime for each of these functions.
e.g. O(1), O(log n), O(n), O(n log n), O(n^2), O(n^3), ... O(2^n)...
-I want the worst-case upper bound


def bigoh1(n):
  sum = 0
  for i in range(100, n):
    sum = sum+1

  print(sum)


O(n)


def bigoh2(n):
  sum = 0
  for i in range(1, n // 2):
    sum = sum + 1
  for j in range(1, n * n):
    sum = sum + 1
  
  print(sum)

First loop is n steps, second is n^2 steps.
n+n^2 = o(n^2)


def bigoh3(n):
  sum = 0
  if n % 2 == 0:
    for j in range(1, n * n):
      sum = sum + 1
  else:
    for k in range(5, n + 1):
      sum = sum + k

  print(sum)

If n is even, we do n^2 work. If n is odd, we do n work.
Remember that we want the worst-case.
O(n^2)


def bigoh4(m, n):
  sum = 0
  for i in range(1, n + 1):
    for j in range(1, m + 1):
      sum = sum + 1
  
  print(sum)

O(n*m)

Not O(n^2). Not O(m^2).

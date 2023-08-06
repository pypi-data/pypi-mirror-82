# lazyRecursion

Usage Example:

```python
>>> from lazyRecursion import RecursiveSequence
>>> 
>>> fibonacci = RecursiveSequence(
...     induction_start={0: 1, 1:1},
...     relative_indices=[-2,-1],
...     recursion_function=lambda x1,x2: x1+x2,
...     cache_file='fib_cache.json' # (optional) deactivates caching if missing
... )
>>> fibonacci[:10]
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

```python
>>> linear = RecursiveSequence(
...     induction_start={0:0},
...     relative_indices=[-1],
...     recursion_function=lambda x: x+5,
... )
>>> linear[:5]
[0, 5, 10, 15, 20]
```

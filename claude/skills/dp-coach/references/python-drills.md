# Python Drills Reference

## Sub-Skills Taxonomy

### Data Structures (Beginner)
- List indexing/slicing
- Dictionary access/manipulation
- Set operations
- Tuple unpacking

### Comprehensions (Intermediate)
- List comprehensions with filter
- Dict comprehensions
- Nested comprehensions
- Generator expressions

### Functions (Intermediate)
- Default/keyword arguments
- *args/**kwargs
- Closures
- Decorators (no args)
- Decorators (with args)

### Iteration (Intermediate)
- enumerate/zip
- itertools basics (chain, combinations)
- Custom iterators
- Generator functions

### Recursion (Intermediate-Advanced)
- Base case identification
- Tree traversal
- Memoization
- Tail recursion patterns

### OOP (Advanced)
- Dunder methods
- Property decorators
- Class methods vs static
- Inheritance/MRO

### Async (Advanced)
- async/await basics
- asyncio.gather
- Async context managers

## Exercise Templates

### List Comprehension Drill
```python
# Transform this loop into a list comprehension
result = []
for x in items:
    if condition(x):
        result.append(transform(x))
```
Variations: nested loops, multiple conditions, dict output

### Recursion Drill
```python
# Implement without loops
def flatten(nested_list):
    """Flatten arbitrarily nested list."""
    pass

# Test cases
assert flatten([1, [2, [3, 4], 5]]) == [1, 2, 3, 4, 5]
assert flatten([]) == []
assert flatten([[[1]]]) == [1]
```

### Decorator Drill
```python
# Create decorator that [logs/times/retries/caches]
@your_decorator
def target_function():
    pass
```

## Difficulty Calibration

| Level | Characteristics |
|-------|----------------|
| 1 | Single concept, obvious solution |
| 2 | Single concept, edge cases |
| 3 | Concept combination, moderate complexity |
| 4 | Non-obvious approach required |
| 5 | Multiple advanced concepts, optimization needed |

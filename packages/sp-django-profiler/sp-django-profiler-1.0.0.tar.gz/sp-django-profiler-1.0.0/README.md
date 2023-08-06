# django-profiler
Useful tool to profile code and Django queries.

### Example
```python
from django_profiler.profile import Profiler

with Profiler(name='my-profiler'):
    print("Hello World!")
```
#### Output:
```
Hello World!

Profiler: my-profiler
 
Number of Queries : 0
Finished in : 0.00s
         2 function calls in 0.000 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 profiling.py:45(__exit__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

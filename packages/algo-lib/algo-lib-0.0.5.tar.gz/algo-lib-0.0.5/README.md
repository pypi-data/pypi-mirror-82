# Algo-lib (the Algorithm Library)

This is a simple example package. It contains two searching algorithms. The purpose of this repo is to practice packaging a library for distribution.

For package distribution information and release history, see: https://pypi.org/project/algo-lib/ 

### Quick Start

1. Install algo-lib from the command line using pip.
```
python3 -m pip install --upgrade algo-lib
```

#### Example Usage

1. Binary Search
```python
from algo_lib import search

lst = [1, 50, 99, 150, 40000]
targetValue = 99

#binary search returns the index of a target value if present in a sorted list
targetIndex = search.binary(lst, 0, len(lst) - 1, targetValue) #targetIndex is 2
```

2. Linear Search
```python
from algo_lib import search

lst = [5, 1, 2, 100, 41, -1]
targetValue = -1

#linear search returns the index of a target value if present in list
targetIndex = search.binary(lst, targetValue) #targetIndex is 5
```

3. Merge Sort
```python
from algo_lib import sort

lst = [5, 1, 2, 100, 41, -1]

#merge sort takes a list argument, and sorts it in either increasing or decreasing order
targetIndex = sort.merge(lst) #lst is [-1, 1, 2, 5, 41, 100]
```
# Simple functions to compare version numbers as strings
# Based on code from: https://www.geeksforgeeks.org/compare-two-version-numbers/

def _process_version_strings(v1: str, v2: str):

    '''Takes two version strings as inputs, returns tuple with lists of integers.'''
    # split the versions by '.'
    arr1 = v1.split('.')
    arr2 = v2.split('.')
    l1 = len(arr1)
    l2 = len(arr2)

    # convert to integers
    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]

    # pad list with zeros if necessary
    if l1>l2:
        for i in range(l2, l1):
            arr2.append(0)
    elif l2>l1:
        for i in range(l1, l2):
            arr1.append(0)

    return arr1, arr2

def is_higher(v1: str, v2: str) -> bool:
    '''Compares two version number strings. Returns True if v1 > v2, or False otherwise.
    Version numbers must contain only digits and periods.'''
    arr1, arr2 = _process_version_strings(v1, v2)
    for i in range(len(arr1)):
        if arr1[i] > arr2[i]:
            return True
    return False

def is_lower(v1: str, v2: str) -> bool:
    '''Compares two version number strings. Returns True if v1 < v2, or False otherwise.
    Version numbers must contain only digits and periods.'''
    arr1, arr2 = _process_version_strings(v1, v2)
    for i in range(len(arr1)):
        if arr1[i] < arr2[i]:
            return True
    return False

def is_equal(v1: str, v2: str) -> bool:
    '''Compares two version number strings. Returns True if v1 == v2, or False otherwise.
    Version numbers must contain only digits and periods.'''
    arr1, arr2 = _process_version_strings(v1, v2)
    for i in range(len(arr1)):
        if not arr1[i] == arr2[i]:
            return False
    return True
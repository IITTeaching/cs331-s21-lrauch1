from unittest import TestCase
import random

def quicksort(lst,pivot_fn):
    qsort(lst,0,len(lst) -1,pivot_fn)

def qsort(lst,low,high,pivot_fn):
    ### BEGIN SOLUTION
    if low < high:
        p = pivot_fn(lst,low,high)
        qsort(lst,low,p-1,pivot_fn)
        qsort(lst,p+1,high,pivot_fn)
    ### END SOLUTION

def pivot_first(lst,low,high):
    ### BEGIN SOLUTION
    pivot = lst[low]
    i = high
    for j in range(high,low,-1):
        if lst[j] > pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i = i-1
    lst[i],lst[low] = lst[low], lst[i]
    return i
    ### END SOLUTION

def pivot_random(lst,low,high):
    ### BEGIN SOLUTION
    r = random.randint(low,high)
    pivot = lst[r]
    lst[r],lst[low] = lst[low], lst[r]
    i = high
    for j in range(high,low,-1):
        if lst[j] > pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i = i-1
    lst[i],lst[low] = lst[low], lst[i]
    return i
    ### END SOLUTION

def pivot_median_of_three(lst,low,high):
    ### BEGIN SOLUTION
    m = median(lst, low, ((low + high) // 2), high)
    pivot = lst[m]
    lst[m],lst[low] = lst[low], lst[m]
    i = high
    for j in range(high,low,-1):
        if lst[j] > pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i = i-1
    lst[i],lst[low] = lst[low], lst[i]
    return i
    ### END SOLUTION

def median(lst,i,j,k):
    u = lst[i]
    v = lst[j]
    w = lst[k]
    if ( u < v and u > w ) or ( u > v and u < w):
        return i
    elif ( v < u and v > w ) or ( v > u and v < w):
        return j
    elif ( u < w and v > w ) or ( w > u and v > w):
        return k
    return i

################################################################################
# TEST CASES
################################################################################
def randomize_list(size):
    lst = list(range(0,size))
    for i in range(0,size):
        l = random.randrange(0,size)
        r = random.randrange(0,size)
        lst[l], lst[r] = lst[r], lst[l]
    return lst

def test_lists_with_pfn(pfn):
    lstsize = 20
    tc = TestCase()
    exp = list(range(0,lstsize))

    lst = list(range(0,lstsize))
    quicksort(lst, pivot_first)
    tc.assertEqual(lst,exp)

    lst = list(reversed(range(0,lstsize)))
    quicksort(lst, pivot_first)
    tc.assertEqual(lst,exp)

    for i in range(0,100):
        lst = randomize_list(lstsize)
        quicksort(lst, pfn)
        tc.assertEqual(lst,exp)

# 30 points
def test_first():
    test_lists_with_pfn(pivot_first)

# 30 points
def test_random():
    test_lists_with_pfn(pivot_random)

# 40 points
def test_median():
    test_lists_with_pfn(pivot_median_of_three)

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_first,
              test_random,
              test_median]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()

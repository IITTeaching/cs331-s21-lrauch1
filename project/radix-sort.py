import urllib
import random
import urllib.request

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    l = book_to_words(book_url)
    maximum = max(l)
    l = padLength(l,maximum)
    for i in range(maximum):
        l = toArray(toQueue(l,i),len(l))
    l = changeAlphabetical(l)
    l = unPadList(l)
    return l

def padLength(lst,length):
    arr = []
    fix = " "
    fixed = fix.encode('ascii','replace')
    for i in range(len(lst)):
        v = lst[i]
        while not len(v) == length:
            v = v + fixed
        arr.append(v)
    return arr

def unPadList(lst):
    arr = []
    for i in range(len(lst)):
        v = lst[i]
        v = v.strip(b' ')
        arr.append(v)
    return arr


def changeAlphabetical(lst):
    queue = []
    for i in range(256):
        l = []
        queue.append(l)
    for j in range(len(lst)):
        n = lst[j][0]
        queue[n].append(lst[j])
    sort = toArray(queue,len(lst))
    return sort

def max(lst):
    maximum = len(lst[0])
    for i in range(1, len(lst)):
        num = lst[i]
        if len(num) > maximum:
            maximum = len(num)
    return maximum

def toArray(lst,length):
    sort = [None] * length
    n = 0
    for i in range(len(lst)):
        j = 0
        while j < len(lst[i]):
            if not lst[i][j] == None:
                num = lst[i].pop(j)
                sort[n] = num
                n+=1
            else:
                j+=1
    return sort


#queue.pop(0) = dequeue
def toQueue(lst,k):
    queue = []
    for i in range(256):
        l = []
        queue.append(l)
    for j in range(len(lst)):
        n = getPlace(lst[j],k)
        queue[n].append(lst[j])
    
    return queue

def getPlace(val,k):
    if len(val) <= 0:
        return 0
    elif k == 0:
        return val[len(val)-1]
    else:
        f = k - 1
        return getPlace(val[0:len(val)-1],f)

################################################################################
# TEST CASES
################################################################################

def test_book():
    arr = book_to_words()
    lst = radix_a_book()
    arr = sorted(arr)
    n = 0
    for i in range(len(arr)):
        if not arr[i]==lst[i]:
            print("Python Sort")
            print(arr[i])
            print()
            print("Radix Sort")
            print(lst[i])
            raise Exception
        n+=1
        print("Correct Comparisons = " + str(n))



def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_book]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()


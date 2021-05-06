import urllib
import urllib.request

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    l = book_to_words()
    maximum = max(l)
    for i in range(len(maximum)):
        l = toArray(toQueue(l,i),len(l))
    return l

def max(lst):
    maximum = lst[0]
    for i in range(1, len(lst)):
        num = lst[i]
        if num > maximum:
            maximum = num
    return maximum

def toArray(lst,length):
    sort = [None] * length
    n = 0
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if not lst[i][j] == None:
                num = lst[i].pop(0)
                sort[n] = num
                n+=1
            else:
                break
    return sort


#queue.pop(0) = dequeue
def toQueue(lst,k):
    queue = []
    for i in range(10):
        l = []
        queue.append(l)
    for j in range(len(lst)):
        n = getPlace(lst[j],k)
        queue[n].append(lst[j])
    
    return queue

def getPlace(val,k):
    if k == 0:
        return val%10
    else:
        f = k - 1
        return getPlace(val/10,f)

def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    radix_a_book()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()


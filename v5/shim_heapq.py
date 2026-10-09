def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem

def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    childpos = 2 * pos + 1
    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2 * pos + 1
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)

def heappush(heap, item):
    heap.append(item)
    _siftdown(heap, 0, len(heap) - 1)

def heappop(heap):
    last = heap.pop()
    if heap:
        ret = heap[0]
        heap[0] = last
        _siftup(heap, 0)
        return ret
    return last

def heapreplace(heap, item):
    ret = heap[0]
    heap[0] = item
    _siftup(heap, 0)
    return ret

def heappushpop(heap, item):
    if heap and heap[0] < item:
        item, heap[0] = heap[0], item
        _siftup(heap, 0)
    return item

def heapify(x):
    n = len(x)
    for i in reversed(range(n // 2)):
        _siftup(x, i)

def nlargest(n, iterable, key=None):
    return sorted(iterable, key=key, reverse=True)[:n]

def nsmallest(n, iterable, key=None):
    return sorted(iterable, key=key)[:n]

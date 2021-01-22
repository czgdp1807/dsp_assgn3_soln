from datastructsalgo import BinaryHeap

def modify_heaps(min_heap, max_heap, curr_num, k):
    min_heap.insert(curr_num)
    max_heap.insert(curr_num)
    if min_heap.heap._num > k:
        min_heap.extract()
    if max_heap.heap._num > k:
        max_heap.extract()
    large, small = (max_heap.heap[0].key, min_heap.heap[0].key)
    return large, small

min_heap = BinaryHeap(heap_property='min')
max_heap = BinaryHeap(heap_property='max')

k = int(input())
curr_num = int(input())
while curr_num != 0:
    large, small = modify_heaps(min_heap, max_heap, curr_num, k)
    print(large, small)
    curr_num = int(input())
large, small = modify_heaps(min_heap, max_heap, curr_num, k)
print(large, small)

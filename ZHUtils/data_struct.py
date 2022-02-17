from heapq import heapify, heappush, heappushpop, nlargest

class MaxHeap(object):
    def __init__(self, top_n):
        self.h = []
        self.length = top_n
        heapify( self.h)
        
    def add(self, element):
        if len(self.h) < self.length:
            heappush(self.h, element)
        else:
            heappushpop(self.h, element)
            
    def getTop(self, n):
        if n< self.length:
            return nlargest(n, self.h)
        return nlargest(self.length, self.h)

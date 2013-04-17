class Graph:
    def __init__(self, head):
        self.head = head

class Node:
    def __init__(self, data, adjacent):
        self.data = data
        self.adjacent = adjacent

    #TODO: string representation
    def __str__(self):
        return str(self.data)

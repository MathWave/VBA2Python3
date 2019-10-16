class Stack:
    def __init__(self):
        self.items = []

    def index(self, n):
        return self.items[-n - 1]

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)
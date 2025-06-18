class Stack:
    __vals = []
    __size = 0

    def push(self, val):
        self.__size += 1
        self.__vals.append(val)

    def pop(self):
        self.__size -= 1
        return self.__vals.pop()

    def peek(self):
        return self.__vals[-1]

    def isEmpty(self):
        return self.__vals == []

    def getVals(self):
        return self.__vals

    def __len__(self):
        return self.__size

    def __iter__(self):
        return iter(self.__vals)

    def __contains__(self, item):
        return item in self.__vals

class Stack:
    class Element:
        def __init__(self, val=None):
            self.value = val
            self.prev_element = None

    def __init__(self, args=None):
        self.__size = 0
        self.__cursor = None
        if args:
            for el in args:
                self.push(el)

    def push(self, val):
        new_element = self.Element(val)
        new_element.prev_element = self.__cursor
        self.__cursor = new_element
        self.__size += 1

    def pop(self):
        if self.is_empty():
            raise Exception('Stack is empty, cant pop item')
        poped_element = self.__cursor
        self.__cursor = poped_element.prev_element
        self.__size -= 1
        return poped_element.value

    def __str__(self) -> str:
        if self.is_empty():
            return ''
        init_element = self.__cursor.prev_element
        result = str(self.__cursor.value)
        while init_element:
            result += ', ' + str(init_element.value)
            init_element = init_element.prev_element
        return result[::-1]

    def peek(self) -> Element:
        return self.__cursor.value

    def is_empty(self) -> bool:
        return self.__size == 0

    def size(self) -> int:
        return self.__size


class BalanceChecker:
    class Bracket:
        __open_brackets = ['(', '{', '[']
        __close_brackets = [')', '}', ']']

        def __init__(self, val):
            self.__val = val
            self.__is_open = val in self.__open_brackets
            if self.__is_open:
                self.__open = self.__val
                self.__close = self.__close_brackets[self.__open_brackets.index(self.__val)]
            else:
                self.__open = self.__open_brackets[self.__close_brackets.index(self.__val)]
                self._close = self.__val

        def get(self):
            return self.__val

        def __str__(self) -> str:
            return self.__val

        def __repr__(self) -> str:
            return self.__str__()

        def is_open(self) -> bool:
            return self.__is_open

        def is_pair(self, val) -> bool:
            if isinstance(val, self.__class__):
                val = val.get()
            if self.__is_open:
                return self.__open_brackets.index(self.__val) == self.__close_brackets.index(val)
            return self.__close_brackets.index(self.__val) == self.__open_brackets.index(val)

    def __init__(self, args):
        self.__stack = Stack([
            self.Bracket(el)
            for el in args

        ])

    def check(self):
        if self.__stack.size() % 2 != 0 or self.__stack.peek().is_open():
            print('Несбалансированно')
            return False
        close_brackets = Stack()
        while True:
            cursor = self.__stack.pop()
            if cursor.is_open():
                if not close_brackets.pop().is_pair(cursor):
                    print('Несбалансированно')
                    return False
            else:
                close_brackets.push(cursor)

            if self.__stack.is_empty() and close_brackets.is_empty():
                print('Сбалансированно')
                return True
            elif self.__stack.is_empty() and not close_brackets.is_empty():
                print('Несбалансированно')
                return False


if __name__ == '__main__':
    ch = BalanceChecker('}{}')
    ch.check()

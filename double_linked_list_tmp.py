from typing import Any, Sequence, Optional

"""
Двусвязный список на основе односвязного списка.

    Самостоятельное задание. В двусвязном списке должны быть следующие методы:
    - **`__str__`**
    - **`__repr__`**
    - **`__getitem__`**
    - **`__setitem__`**
    - **`__len__`**
    - **`insert`**
    - **`index`**
    - **`remove`**
    - **`append`**
    - **`__iter__`**

    Необязательно все эти методы должны быть переопределены в явном виде. По максимуму используйте
    наследование, если поведение списков в контексте реализации указанных метод схоже.
    С точки зрения наследования по минимуму перегружайте методы. При необходимости рефакторите базовый класс,
    чтобы локализовать части кода во вспомогательные функции, которые имеют различное поведение
    в связном и двусвязном списках.
    Стремитесь к минимизации кода в дочернем классе.

    Есть какой-то метод класса DoubleLinkedList хотите отработать в явном виде ещё раз, не возбраняется.
"""


# ToDo импорт любой вашей реалиазации LinkedList


class LinkedList:
    class Node:
        """
        Внутренний класс, класса LinkedList.

        Пользователь напрямую не работает с узлами списка, узлами оперирует список.
        """

        def __init__(self, value: Any, next_: Optional['Node'] = None):
            """
            Создаем новый узел для односвязного списка

            :param value: Любое значение, которое помещено в узел
            :param next_: следующий узел, если он есть
            """
            self.value = value
            self.next = next_  # Вызывается сеттер

        @property
        def next(self):
            """Getter возвращает следующий узел связного списка"""
            return self.__next

        @next.setter
        def next(self, next_: Optional['Node']):
            """Setter проверяет и устанавливает следующий узел связного списка"""
            self.__next = next_

        def _check_node(self, node):
            if not isinstance(node, self.__class__) and node is not None:
                msg = f"Устанавливаемое значение должно быть экземпляром класса {self.__class__.__name__} " \
                      f"или None, не {node.__class__.__name__}"
                raise TypeError(msg)

        def __repr__(self):
            """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
            return f"Node({self.value}, {self.next})"

        def __str__(self):
            """Вызывается функциями str, print и format. Возвращает строковое представление объекта."""
            return f"{self.value}"

    def __init__(self, data: Sequence = None):
        """Конструктор связного списка"""
        self.__len = 0
        self.head = None  # Node
        self.tail = None

        if self.is_iterable(data):  # ToDo Проверить, что объект итерируемый. Метод self.is_iterable
            for value in data:
                self.append(value)

    def __str__(self):
        """Вызывается функциями str, print и format. Возвращает строковое представление объекта."""
        return f"{[value for value in self]}"

    def __repr__(self):
        """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
        return f"{self.__class__.__name__}({[value for value in self]})"

    def __len__(self):
        return self.__len

    def __step_by_step_on_nodes(self, index):
        if not isinstance(index, int):
            raise TypeError(f"Index must be {int.__name__} not {index.__class__.__name__}")

        if index < 0:
            index += self.__len

        if not -self.__len <= index < self.__len:
            raise IndexError(f"{self.__class__.__name__} index out of range")

        current_node = self.head

        for _ in range(index):
            current_node = current_node.next

        return current_node

    def __getitem__(self, index: int) -> Any:
        print(f'Method __getitem__ called')
        current_node = self.__step_by_step_on_nodes(index)

        return current_node.value

    def __setitem__(self, key, value: Any):
        current_node = self.__step_by_step_on_nodes(key)
        current_node.value = value

    def __reversed__(self):
        return iter(self[::-1])

    def __value_iterator(self):
        """
        Generator
        """
        current_node = self.head
        for _ in range(self.__len):
            yield current_node
            current_node = current_node.next
            # if current_node.next.value is None:
            #     raise StopIteration

    def __iter__(self):
        print(f'Method __iter__ called')
        return self.__value_iterator()

    # def __next__(self):
    #     print(f'Method __next__ called')
    #     if self.current_iter_node is None:
    #         raise StopIteration
    #
    #     value = self.current_iter_node.value
    #     self.current_iter_node = self.current_iter_node.next
    #
    #     return value

    def append(self, value: Any):
        """Добавление элемента в конец связного списка"""
        append_node = self.Node(value)
        if self.head is None:
            self.head = append_node
            self.tail = append_node
        else:
            self.__linked_nodes(self.tail, append_node)
            self.tail = append_node

        self.__len += 1

    @staticmethod
    def __linked_nodes(left: Node, right: Optional[Node]) -> None:
        left.next = right

    def to_list(self) -> list:
        return [value for value in self]

    def insert(self, index: int, value: Any) -> None:
        if not isinstance(index, int):
            raise TypeError()

        if index == 0:
            insert_node = self.Node(value)
            self.__linked_nodes(insert_node, self.head)
            self.head = insert_node
            self.__len += 1

        elif 0 < index < self.__len:
            prev_node = self.__step_by_step_on_nodes(index - 1)
            current_node = prev_node.next
            insert_node = self.Node(value, next_=current_node)
            self.__linked_nodes(prev_node, insert_node)
            self.__len += 1

        elif index > self.__len - 1:
            self.append(value)

    def clear(self) -> None:
        self.head = None
        self.__len = 0

    def index(self, value: Any) -> int:
        print(f'{self.index.__name__} function called')
        index = 0
        for _ in self:
            if self[index] == value:
                return index
            elif index == self.__len - 1:
                raise ValueError(f"{value} is not in {self.__class__.__name__}")
            index += 1

    def remove(self, value: Any) -> None:
        index = self.index(value)
        if index == 0:
            self[index] = None
            self.head = self.__step_by_step_on_nodes(index + 1)
            self.__len -= 1

        elif 0 < self.index(value) < self.__len:
            prev_node = self.__step_by_step_on_nodes(index - 1)
            remove_node = prev_node.next
            next_node = remove_node.next
            self.__linked_nodes(prev_node, next_node)
            self.__len -= 1

        elif self.index(value) == self.__len - 1:
            self.tail = None
            self.__len -= 1

    def sort(self) -> None:
        flag = True
        iterations = 0
        while flag:
            flag = False
            for i in range(self.__len - iterations - 1):
                current_node = self.__step_by_step_on_nodes(i)
                if not isinstance(current_node.value, type(current_node.next.value)):
                    raise TypeError(f'Cannot compare {current_node} and {current_node.next}')
                if current_node.value > current_node.next.value:
                    current_node.value, current_node.next.value = current_node.next.value, current_node.value
                    flag = True
            iterations += 1

    @staticmethod
    def is_iterable(data) -> bool:
        """Метод для проверки является ли объект итерируемым"""
        if hasattr(data, '__iter__'):
            return True
        else:
            raise AttributeError(f'{data.__class__.__name__} is not iterable')

    def __contains__(self, item: Any):
        return any(item == value for value in self)


class DoubleLinkedList(LinkedList):
    class DoubleLinkedNode(LinkedList.Node):
        def __init__(self, value: Any,
                     next_: Optional['Node'] = None,
                     prev: Optional['Node'] = None
                     ):
            # ToDo расширить возможности базового конструктора с учетом особенностей двусвязного списка
            super().__init__(value, next_)
            self.prev = prev

        def __repr__(self) -> str:
            """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
            # ToDo перегрузить метод
            return f"{self.__class__.__name__}({self.value}, {self.next}, {self.prev})"

        @property
        def prev(self):
            """Getter возвращает следующий узел связного списка"""
            return self.__prev

        @prev.setter
        def prev(self, prev: Optional['Node']):
            """Setter проверяет и устанавливает следующий узел связного списка"""
            self._check_node(prev)
            self.__prev = prev

    def __init__(self, data: Sequence = None):
        """Конструктор связного списка"""
        super().__init__(data)
        ...

    # - **`__str__`**
    # - **`__repr__`**
    # - **`__getitem__`**
    # - **`__setitem__`**
    # - **`__len__`**
    # - **`insert`**
    # - **`index`**
    # - **`remove`**
    # - **`append`**
    # - **`__iter__`**


if __name__ == '__main__':
    ll = LinkedList([1, 2, 3, 4, 5, 6, 7])
    dll = DoubleLinkedList([1, 2, 3, 4, 5, 6, 7])
    print(dll)
    print(ll)


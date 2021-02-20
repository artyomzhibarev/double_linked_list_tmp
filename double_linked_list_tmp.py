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


# ToDo импорт любой вашей реализации LinkedList


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
            return f"{self.__class__.__name__}({self.value}, {self.next})"

        def __str__(self):
            """Вызывается функциями str, print и format. Возвращает строковое представление объекта."""
            return f"{self.value}"

    def __init__(self, data: Sequence = None):
        """Конструктор связного списка"""
        self._len = 0
        self.head = None  # Node
        self.tail = None

        if self._is_iterable(data):  # ToDo Проверить, что объект итерируемый. Метод self.is_iterable
            for value in data:
                self.append(value)
                # print(f"Element {value} has been added to {self.__class__.__name__}")

    def __str__(self):
        """Вызывается функциями str, print и format. Возвращает строковое представление объекта."""
        return f"{[value for value in self]}"

    def __repr__(self):
        """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
        return f"{self.__class__.__name__}({[value for value in self]})"

    def __len__(self):
        return self._len

    def __step_by_step_on_nodes(self, index):
        print(f'Method {self.__step_by_step_on_nodes.__name__} called')
        if not isinstance(index, int):
            raise TypeError(f"Index must be {int.__name__} not {index.__class__.__name__}")

        if not -self._len < index < self._len:
            raise IndexError(f'IndexError: {self.__class__.__name__} assignment index out of range')

        if index < 0:
            index += self._len  # Todo Сделать функцию проверки индекса для __delitem__

        current_node = self.head
        for _ in range(index):
            current_node = current_node.next
        return current_node

    def __getitem__(self, key: int) -> Any:
        print(f'Method {self.__getitem__.__name__} called')
        current_node = self.__step_by_step_on_nodes(key)
        return current_node.value

    def __setitem__(self, key, value: Any):
        print(f'Method {self.__setitem__.__name__} called')
        current_node = self.__step_by_step_on_nodes(key)
        current_node.value = value

    def __delitem__(self, key):
        print(f'Method {self.__delitem__.__name__} called')
        if key < 0:
            key += self._len
        if 0 < key < self._len - 1:
            prev_node = self.__step_by_step_on_nodes(key - 1)
            delete_node = prev_node.next
            next_node = delete_node.next
            delete_node = None
            self.__linked_nodes(prev_node, next_node)
            self._len -= 1
        if key == 0:
            self.head = self.__step_by_step_on_nodes(key)
            self.head = self.head.next
            self._len -= 1
        if key == self._len - 1:
            prev_node = self.__step_by_step_on_nodes(key - 1)
            delete_node = prev_node.next
            delete_node = None
            self.tail = prev_node
            self._len -= 1

    def __reversed__(self):
        return iter(self[::-1])

    def _value_iterator(self):
        """
        Node value generator
        """
        print(f'The {self._value_iterator.__name__} method of the {self.__class__.__name__} is called')
        current_node = self.head
        for _ in range(self._len):
            yield current_node.value
            current_node = current_node.next

    def __iter__(self):
        print(f'The {self.__iter__.__name__} method of the {self.__class__.__name__} is called')
        return self._value_iterator()

    def append(self, value: Any):
        # print(f'The {self.append.__name__} method of the {self.__class__.__name__} is called')
        """Добавление элемента в конец связного списка"""
        append_node = self.Node(value)
        if self.head is None:
            self.tail = append_node
            self.head = append_node
        else:
            self.__linked_nodes(self.tail, append_node)
            self.tail = append_node

        self._len += 1

    @staticmethod
    def __linked_nodes(left: Node, right: Optional[Node]) -> None:
        left.next = right

    def to_list(self) -> list:
        return [value for value in self]

    def insert(self, index: int, value: Any) -> None:
        print(f'{self.insert.__name__} function called')
        if not isinstance(index, int):
            raise TypeError()

        if index == 0:
            insert_node = self.Node(value)
            self.__linked_nodes(insert_node, self.head)
            self.head = insert_node
            self._len += 1

        elif 0 < index < self._len:
            prev_node = self.__step_by_step_on_nodes(index - 1)
            current_node = prev_node.next
            insert_node = self.Node(value, next_=current_node)
            self.__linked_nodes(prev_node, insert_node)
            self._len += 1

        elif index > self._len - 1:
            self.append(value)

    def clear(self) -> None:
        self.head = None
        self._len = 0

    def index(self, value: Any) -> int:
        print(f'{self.index.__name__} function called')
        current_node = self.head
        for index in range(self._len):
            if current_node.value == value:
                return index
            else:
                current_node = current_node.next
        raise ValueError(f"{value} is not in {self.__class__.__name__}")

    def remove(self, value: Any) -> None:
        print(f'{self.remove.__name__} function called')
        index = self.index(value)
        if index == 0:
            self.head = self.head.next
            self._len -= 1

        elif 0 < index < self._len - 1:
            prev_node = self.__step_by_step_on_nodes(index - 1)
            remove_node = prev_node.next
            next_node = remove_node.next
            self.__linked_nodes(prev_node, next_node)
            self._len -= 1

        elif index == self._len - 1:
            self.tail = self.__step_by_step_on_nodes(index - 1)
            self.tail.next = None
            self._len -= 1
            print(self.tail)

    def sort(self) -> None:
        flag = True
        iterations = 0
        while flag:
            flag = False
            for i in range(self._len - iterations - 1):
                current_node = self.__step_by_step_on_nodes(i)
                if not isinstance(current_node.value, type(current_node.next.value)):
                    raise TypeError(f'Cannot compare {current_node} and {current_node.next}')
                if current_node.value > current_node.next.value:
                    current_node.value, current_node.next.value = current_node.next.value, current_node.value
                    flag = True
            iterations += 1

    @staticmethod
    def _is_iterable(data):
        """Метод для проверки является ли объект итерируемым"""
        if not hasattr(data, '__iter__'):
            raise AttributeError(f'{data.__class__.__name__} is not iterable')
        else:
            return True

    def __contains__(self, item: Any):
        return any(item == value for value in self)


if __name__ == '__main__':
    ll = LinkedList([1, 2, 3, 4, 5, 6, 7])
    ll.remove(7)
    print(ll)

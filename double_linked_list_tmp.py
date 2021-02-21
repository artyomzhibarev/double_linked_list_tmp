from typing import Any, Sequence, Optional
from linked_list_clear import LinkedList
import sys

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


class DoubleLinkedList(LinkedList):
    class DoubleLinkedNode(LinkedList.Node):
        """Конструктор DoubleLinkedNode"""
        def __init__(self, value: Any,
                     next_: Optional['Node'] = None,
                     prev: Optional['Node'] = None):
            # ToDo расширить возможности базового конструктора с учетом особенностей двусвязного списка
            super().__init__(value, next_)
            self._prev = prev

        def __repr__(self) -> str:
            """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
            # ToDo перегрузить метод
            return f"{self.__class__.__name__}({self.value}, {self.next}, {self.prev})"

        @property
        def prev(self):
            """Getter возвращает следующий узел связного списка"""
            return self._prev

        @prev.setter
        def prev(self, prev: Optional['Node']):
            """Setter проверяет и устанавливает следующий узел связного списка"""
            self._check_node(prev)
            self._prev = prev

    def __init__(self, data: Sequence = None):
        """Конструктор DoubleLinkedList"""
        super().__init__(data)

    def __repr__(self):
        """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
        return f"{self.__class__.__name__}({[value for value in self]})"

    @staticmethod
    def __linked_nodes(left: DoubleLinkedNode, right: Optional[DoubleLinkedNode]) -> None:
        left.next = right
        right.prev = left

    def __step_by_step_on_nodes_forward(self, index):
        self.__step_by_step_check(index)
        current_node = self.head
        for _ in range(index):
            current_node = current_node.next
        return current_node

    def __step_by_step_on_nodes_backforward(self, index):
        self.__step_by_step_check(index)
        current_node = self.tail
        for _ in range(self._len - index - 1):
            current_node = current_node.prev
        return current_node

    def __step_by_step_check(self, index):
        if not isinstance(index, int):
            raise TypeError(f"Index must be {int.__name__} not {index.__class__.__name__}")
        if not -self._len < index < self._len:
            raise IndexError(f'IndexError: {self.__class__.__name__} assignment index out of range')
        if index < 0:
            index += self._len

    # def insert(self, index: int, value: Any) -> None:
    #     if not isinstance(index, int):
    #         raise TypeError()
    #
    #     if index < 0:
    #         index += self._len
    #
    #     if index == 0:
    #         insert_node = self.DoubleLinkedNode(value)
    #         self.__linked_nodes(insert_node, self.head)
    #         self.head = insert_node
    #         self._len += 1
    #
    #     elif 0 < index <= self._len // 2:
    #         prev_node = self.__step_by_step_on_nodes_forward(index - 1)
    #         current_node = prev_node.next
    #         insert_node = self.DoubleLinkedNode(value, next_=current_node)
    #         self.__linked_nodes(prev_node, insert_node)
    #         self._len += 1
    #
    #     elif self._len // 2 < index < self._len:
    #         next_node = self.__step_by_step_on_nodes_backforward(index + 1)
    #         current_node = next_node.prev
    #         insert_node = self.DoubleLinkedNode(value, next_=current_node)
    #         self.__linked_nodes(next_node, insert_node)
    #         self._len += 1
    #
    #     elif index >= self._len:
    #         self.append(value)

    # def index(self, value: Any):
    #     current_node = self.head
    #     for index in range(self._len):
    #         if current_node.value == value:
    #             return index
    #         current_node = current_node.next

    # def remove(self, value):
    #     remove_node = self.DoubleLinkedNode(value, )
    #     for index in range(self._len):
    #         if remove_node.value == value:
    #             ...


# - **`remove`**
# - **`append`**
# - **`__iter__`**

if __name__ == '__main__':
    dll = DoubleLinkedList([1, 2, 3, 4, 5])
    print(dll[-5])
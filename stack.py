from typing import List, Optional

class Stack:
    def __init__(self) -> None:
        self.items: List[Optional[str]] = []

    def is_empty(self) -> bool:
        """
        Проверяет, пуст ли стек. Возвращает True, если пуст, иначе False.
        """
        return len(self.items) == 0

    def push(self, item: str) -> None:
        """
        Добавляет элемент на вершину стека.
        """
        self.items.append(item)

    def pop(self) -> Optional[str]:
        """
        Удаляет верхний элемент стека и возвращает его.
        Возвращает None, если стек пуст.
        """
        return self.items.pop() if self.items else None

    def peek(self) -> Optional[str]:
        """
        Возвращает верхний элемент стека, но не удаляет его.
        Возвращает None, если стек пуст.
        """
        return self.items[-1] if self.items else None

    def size(self) -> int:
        """
        Возвращает количество элементов в стеке.
        """
        return len(self.items)

def is_balanced(expression: str) -> bool:
    """
    Проверяет, является ли строка сбалансированной по скобкам.
    """
    stack = Stack()
    open_brackets = "({["
    closed_brackets = ")}]"
    matching_brackets = {')': '(', '}': '{', ']': '['}

    for char in expression:
        # Если символ является открывающей скобкой, добавляем его в стек
        if char in open_brackets:
            stack.push(char)
        # Если символ является закрывающей скобкой, проверяем соответствие
        elif char in closed_brackets:
            if stack.is_empty() or stack.pop() != matching_brackets[char]:
                return False

    # Если стек пуст, значит скобки сбалансированы
    return stack.is_empty()

if __name__ == "__main__":
    expression = '[([])((([[[]]])))]{()}'  # Должно вернуть True
    # expression = '[[{())}]'  # Должно вернуть False
    result = is_balanced(expression)
    print("Сбалансированно" if result else "Несбалансированно")
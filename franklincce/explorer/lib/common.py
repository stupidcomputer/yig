from typing import Any
class FitzBlockWrapper:
    def __init__(self, block):
        self.x0, self.y0, self.x1, \
            self.y1, self.text, \
            self.block_number, self.block_type = block

        self.x0 = int(self.x0)
        self.x1 = int(self.x1)
        self.y0 = int(self.y0)
        self.y1 = int(self.y1)
        self.block_number = int(self.block_number)
        self.block_type = int(self.block_type)

    def __str__(self):
        return str((
            self.x0, self.y0, self.x1, self.y1, self.text
        ))

    def __repl__(self):
        return self.__str__()

def words_in_superstring(words: list[str], superstring: str) -> bool:
    for word in words:
        if not str(word).lower() in str(superstring).lower():
            return False
        return True

def split_by_lambda(arr: list[Any], func):
    output = []
    current = []
    for item in arr:
        if func(item):
            output.append(current)
            current = []
        else:
            current.append(item)

    output.append(current)
    return output

def get_block_by_x_value(arr: list[FitzBlockWrapper], xvalue: int) -> FitzBlockWrapper:
    for item in arr:
        if item.x0 == xvalue:
            return item

def remove_block_by_x_value(arr: list[FitzBlockWrapper], xvalue: int) -> list[FitzBlockWrapper]:
    return [i for i in arr if not i.x0 == xvalue]

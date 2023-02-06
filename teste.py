class Example:
    def __init__(self, items=[]):
        self.items = items

    def add_item(self, item):
        self.items.append(item)


example1 = Example()
example1.add_item(1)
print(example1.items)  # [1]

example2 = Example()
example2.add_item(2)
print(example2.items)  # [2]
print(example1.items)  # [1, 2], não [1] como esperado
